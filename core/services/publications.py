from django.core.exceptions import ValidationError

from core.models import Topic, Scope, DocumentType, Document, Organization

import dateparser


def list_documents(
    topic: int = None,
    scope: int = None,
    document_type: int = None,
    publication_page: int = None,
    source_org: int = None,
    before: str = None,
    after: str = None,
    limit: int = None,
):
    """
    Lists **published** documents, with optional filters
    """
    qs = Document.objects.filter(is_published=True)

    # Filters
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
    if before:
        parsed_date = dateparser.parse(before)
        qs = qs.filter(last_update__lte=parsed_date)
    if after and dateparser.parse(after):
        qs = qs.filter(last_update__gte=after)

    qs = qs.order_by("-weight")
    if limit:
        qs = qs[:limit]
    return qs


def documents_to_cards(qs):
    """
    Converts a queryset of documents to a list of cards
    """
    cards = []
    for doc in qs:
        if len(doc.document_type.all()):
            detail = f"{doc.document_type.all()[0]} | {doc.last_update}"
        else:
            detail = f" Publication | {doc.last_update}"

        if doc.source and len(doc.source.editor.all()):
            detail = f"{detail} • {', '.join([ i.short_name() for i in doc.source.editor.all()])}"
        cards.append(
            {
                "detail": detail,
                "link": doc.url,
                "title": doc.title,
                "description": doc.body,
                "image": doc.image_url,
            }
        )

    return cards


def publication_filters(request):
    """
    Returns a list of filters
    """
    # Model type: select
    models = [
        {
            "name": "Thématique",
            "model": Topic,
            "key": "topic",
            "label": "name",
            "modale": False,
        },
        {
            "name": "Portée",
            "model": Scope,
            "key": "scope",
            "label": "name",
            "modale": False,
        },
        {
            "name": "Type de ressource",
            "model": DocumentType,
            "key": "document_type",
            "label": "name",
            "modale": False,
        },
        {
            "name": "Organisme auteur",
            "model": Organization,
            "key": "source_org",
            "label": "name",
            "modale": True,
        },
    ]
    response = {}
    for m in models:
        values = []
        model_key = m["key"]

        # If the filter is in the "Extra filters" modale, we want to store
        # the result until the "Validate" button is checked
        if m["modale"]:
            onchange_function = f"setModaleParam({model_key})"
        else:
            onchange_function = f"setUrlParam({model_key})"

        entries = m["model"].objects.all()
        for entry in entries:
            if m["label"] == "title":
                entry_text = entry.title
            else:
                entry_text = entry.name
            values.append({"value": str(entry.id), "text": entry_text})

        response[model_key] = {
            "label": m["name"],
            "id": model_key,
            "options": values,
            "selected": request.GET.get(model_key),
            "onchange": onchange_function,
            "default": {"text": f"- {m['name']} -", "disabled": False, "hidden": False},
        }

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

        except ValidationError:
            pass

    if request.GET.get("after"):
        try:
            date_after = request.GET.get("after")
            date_after_parsed = dateparser.parse(date_after)
            if date_after_parsed.date() > date_min:
                date_before_min = date_after
        except ValidationError:
            pass

    response["after"] = {
        "label": "Entre le",
        "id": "after",
        "type": "date",
        "value": date_after,
        "min": date_after_min,
        "max": date_after_max,
        "onchange": f"setModaleParam(after)",
    }
    response["before"] = {
        "label": "Et le",
        "id": "before",
        "type": "date",
        "value": date_before,
        "min": date_before_min,
        "max": date_before_max,
        "onchange": f"setModaleParam(before)",
    }

    # Count the extra filters
    extra_filters_count = 0
    if request.GET.get("source_org"):
        extra_filters_count += 1
    if date_after or date_before:
        extra_filters_count += 1

    response["extra_count"] = extra_filters_count

    return response