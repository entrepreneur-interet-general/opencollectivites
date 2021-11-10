from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from francedata.models import Commune, Departement, Epci, Region
from django.db.models import Max

from core.models import (
    DataYear,
    PageType,
    Topic,
    Scope,
    DocumentType,
    Document,
    Organization,
)

import dateparser


def list_documents(
    topic: int = None,
    scope: int = None,
    document_type: int = None,
    publication_page: int = None,
    source_org: int = None,
    year: int = None,
    commune: str = None,
    epci: str = None,
    departement: str = None,
    region: str = None,
    after: str = None,
    before: str = None,
    limit: int = None,
    offset: int = 0,
) -> QuerySet:
    """
    Lists **published** documents, with optional filters
    """
    qs = Document.objects.filter(is_published=True)

    # Generic filters
    if topic:
        qs = qs.filter(topics__id=topic)
    if scope:
        qs = qs.filter(scope__id=scope)
    if document_type:
        qs = qs.filter(document_type__id=document_type)
    if publication_page:
        qs = qs.filter(publication_pages__id=publication_page)
    if source_org:
        qs = qs.filter(source__editor__id=source_org)
    if year:
        qs = qs.filter(years__year=year)

    # Specific collectivity filters
    if commune:
        qs = qs.filter(communes__slug=commune)
    if epci:
        qs = qs.filter(epcis__slug=epci)
    if departement:
        qs = qs.filter(departements__slug=departement)
    if region:
        qs = qs.filter(regions__slug=region)

    # Date filters
    if before:
        parsed_date = dateparser.parse(before)
        qs = qs.filter(last_update__lte=parsed_date)
    if after and dateparser.parse(after):
        qs = qs.filter(last_update__gte=after)

    qs = qs.annotate(max_year=Max("years__year")).order_by(
        "-weight", "-max_year", "title"
    )

    total_count = qs.count()
    if limit:
        qs = qs[offset : offset + limit]

    return qs, total_count


def documents_to_cards(qs: QuerySet) -> list:
    """
    Converts a queryset of documents to a list of cards
    """
    cards = []
    for doc in qs:
        if doc.document_type.count():
            detail = f"{doc.document_type.first()}"
        else:
            detail = f" Publication"

        if doc.years_range():
            detail = f"{detail} | {doc.years_range()}"

        if doc.source and len(doc.source.editor.all()):
            detail = f"{detail} • {', '.join([ i.short_name() for i in doc.source.editor.all()])}"
        cards.append(
            {
                "detail": detail,
                "link": doc.url,
                "title": doc.title,
                "description": doc.body,
                "image_url": doc.image_url,
            }
        )

    return cards


def publication_filters(request: HttpRequest) -> dict:
    """
    Returns a dict of filters
    """
    # Model type: select
    models = [
        {
            "name": "Thématique",
            "model": Topic,
            "key": "topic",
            "label": "name",
            "id_key": "id",
        },
        {
            "name": "Type de territoire",
            "model": Scope,
            "key": "scope",
            "label": "name",
            "id_key": "id",
        },
        {
            "name": "Type de ressource",
            "model": DocumentType,
            "key": "document_type",
            "label": "name",
            "id_key": "id",
        },
        {
            "name": "Organisme auteur",
            "model": Organization,
            "key": "source_org",
            "label": "name",
            "id_key": "id",
        },
        {
            "name": "Année",
            "model": DataYear,
            "key": "year",
            "label": "year",
            "id_key": "year",
        },
        {
            "name": "Région",
            "model": Region,
            "key": "region",
            "label": "name",
            "id_key": "slug",
        },
        {
            "name": "Département",
            "model": Departement,
            "key": "departement",
            "label": "name",
            "id_key": "slug",
        },
    ]
    response = {}
    filter_tags = []
    for m in models:
        values = []
        model_key = m["key"]
        selected_value = request.GET.get(model_key)

        # Assigning the value name to the value itself in case it references something
        # that doesn't exist.
        selected_value_name = selected_value

        entries = m["model"].objects.all()

        # Sort entries
        if m["label"] == "title":
            entries = entries.order_by("title")
        elif m["label"] == "year":
            entries = entries.order_by("year")
        else:
            entries = entries.order_by("name")

        for entry in entries:
            # Label of the select option
            if m["label"] == "title":
                entry_text = entry.title
            elif m["label"] == "year":
                entry_text = entry.year
            else:
                entry_text = entry.name

            # Value of the select option
            if m["id_key"] == "slug":
                entry_id = entry.slug
            elif m["id_key"] == "year":
                entry_id = str(entry.year)
            else:
                entry_id = str(entry.id)

            if entry_id == selected_value:
                selected_value_name = entry_text

            values.append({"value": entry_id, "text": entry_text})

        response[model_key] = {
            "label": m["name"],
            "id": model_key,
            "options": values,
            "selected": selected_value,
            "onchange": f"setUrlParam({model_key})",
            "default": {"text": f"- {m['name']} -", "disabled": False, "hidden": False},
        }

        if selected_value:
            filter_tags.append(
                {
                    "label": f"{m['name']} : {selected_value_name}",
                    "link": "#",
                    "onclick": f"removeUrlParam('{model_key}');",
                }
            )

    # Model type: date

    ## Last update
    ### The values need to be:
    # - between the extreme values in the database
    # - but also after needs to be < before

    date_min = (
        Document.objects.filter(is_published=True)
        .order_by("last_update")[0]
        .last_update
    )

    date_max = (
        Document.objects.filter(is_published=True)
        .order_by("-last_update")[0]
        .last_update
    )

    date_before = None
    date_before_max = date_max.strftime("%Y-%m-%d")
    date_after = None
    date_after_min = date_min.strftime("%Y-%m-%d")

    date_after_max = date_before_max
    date_before_min = date_after_min

    if request.GET.get("before"):
        try:
            date_before = request.GET.get("before")
            date_before_parsed = dateparser.parse(date_before)
            if date_before_parsed.date() < date_max:
                date_after_max = date_before

            filter_tags.append(
                {
                    "label": f"Avant le : {date_before}",
                    "link": "#",
                    "onclick": f"removeUrlParam('before');",
                }
            )

        except ValidationError:
            pass

    if request.GET.get("after"):
        try:
            date_after = request.GET.get("after")
            date_after_parsed = dateparser.parse(date_after)
            if date_after_parsed.date() > date_min:
                date_before_min = date_after

            filter_tags.append(
                {
                    "label": f"Après le : {date_after}",
                    "link": "#",
                    "onclick": f"removeUrlParam('after');",
                }
            )

        except ValidationError:
            pass

    response["after"] = {
        "label": "Entre le",
        "id": "after",
        "type": "date",
        "value": date_after,
        "min": date_after_min,
        "max": date_after_max,
        "onchange": f"setUrlParam(after)",
    }
    response["before"] = {
        "label": "Et le",
        "id": "before",
        "type": "date",
        "value": date_before,
        "min": date_before_min,
        "max": date_before_max,
        "onchange": f"setUrlParam(before)",
    }

    # Count the extra filters
    extra_filters_count = 0
    if request.GET.get("source_org"):
        extra_filters_count += 1
    if request.GET.get("year"):
        extra_filters_count += 1
    if request.GET.get("departement"):
        extra_filters_count += 1
    if request.GET.get("region"):
        extra_filters_count += 1
    if date_after or date_before:
        extra_filters_count += 1

    response["extra_count"] = extra_filters_count

    # Tags for the special filters (that are in neither form)

    if request.GET.get("publication_page"):
        page = request.GET.get("publication_page")
        page_item = PageType.objects.filter(id=page).first()
        if page_item:
            page_name = page_item.name
        else:
            page_name = page
        filter_tags.append(
            {
                "label": f"Page : {page_name}",
                "link": "#",
                "onclick": f"removeUrlParam('publication_page');",
            }
        )

    if request.GET.get("epci"):
        epci = request.GET.get("epci")
        epci_item = Epci.objects.filter(slug=epci).first()
        if epci_item:
            epci_name = epci_item.name
        else:
            epci_name = epci
        filter_tags.append(
            {
                "label": f"EPCI : {epci_name}",
                "link": "#",
                "onclick": f"removeUrlParam('epci');",
            }
        )

    if request.GET.get("commune"):
        commune = request.GET.get("commune")
        commune_item = Commune.objects.filter(slug=commune).first()
        if commune_item:
            commune_name = commune_item.name
        else:
            commune_name = commune
        filter_tags.append(
            {
                "label": f"Commune : {commune_name}",
                "link": "#",
                "onclick": f"removeUrlParam('commune');",
            }
        )

    response["filter_tags"] = sorted(filter_tags, key=lambda d: d["label"])
    return response


def list_publications_for_collectivity(
    collectivity_type: str, collectivity_slug: str, limit: int = 6
):
    if collectivity_type == "commune":
        level_title = "Utiles à toutes les communes"
        instance_title = "Concernant cette commune"
        publication_page_id = 1
        publications_for_instance, instance_total_count = list_documents(
            commune=collectivity_slug, limit=limit
        )
    elif collectivity_type == "epci":
        level_title = "Utiles à tous les EPCI"
        instance_title = "Concernant cet EPCI"
        publication_page_id = 4
        publications_for_instance, instance_total_count = list_documents(
            epci=collectivity_slug, limit=limit
        )
    elif collectivity_type == "departement":
        level_title = "Utiles à tous les départements"
        instance_title = "Concernant ce département"
        publication_page_id = 2
        publications_for_instance, instance_total_count = list_documents(
            departement=collectivity_slug, limit=limit
        )
    elif collectivity_type == "region":
        level_title = "Utiles à toutes les régions"
        instance_title = "Concernant cette région"
        publication_page_id = 3
        publications_for_instance, instance_total_count = list_documents(
            region=collectivity_slug, limit=limit
        )

    if instance_total_count > limit:
        instance_see_all = True
    else:
        instance_see_all = False

    publications = {"collectivity_type": collectivity_type}
    level = {}
    level["title"] = level_title
    level["publication_page_id"] = publication_page_id
    publications_for_level, level_total_count = list_documents(
        publication_page=publication_page_id, limit=limit
    )
    level["cards"] = documents_to_cards(publications_for_level)
    if level_total_count > limit:
        level["see_all"] = True
    else:
        level["see_all"] = False
    publications["level"] = level

    instance = {}
    instance["title"] = instance_title
    instance["slug"] = collectivity_slug
    instance["cards"] = documents_to_cards(publications_for_instance)
    instance["see_all"] = instance_see_all
    publications["instance"] = instance
    return publications
