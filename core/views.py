from django.urls.base import reverse
from core.services.regions import region_data
from core.services.departements import departement_data
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.http import require_safe

from core.models import Topic, Scope, Source
from core.services.utils import init_payload
from core.services.communes import (
    commune_data,
    communes_compare,
    compare_communes_for_export,
)
from core.services.epcis import epci_data
from core.services.publications import (
    list_documents,
    documents_to_cards,
    publication_filters,
)

from francedata.models import Departement, Region, Commune, Epci


####################
# Basic navigation #
####################


@require_safe
def page_index(request):
    payload = init_payload("Accueil")
    return render(request, "core/index.html", payload)


@require_safe
def error404(request, exception):
    payload = init_payload("Erreur")
    payload["exception"] = exception
    return render(request, "core/404.html", payload, status=404)


@require_safe
def error500(request, *args, **argv):
    payload = init_payload("Erreur serveur")
    return render(request, "core/500.html", payload, status=500)


@require_safe
def error50x(request, *args, **argv):
    payload = init_payload("Erreur serveur")
    return render(request, "core/50x.html", payload, status=503)


@require_safe
def page_not_yet(request, **kwargs):
    payload = init_payload("Page en construction")
    return render(request, "core/page_not_yet.html", payload)


########################
# Places-related pages #
########################


@require_safe
def page_commune_detail(request, slug):
    commune = get_object_or_404(Commune, slug=slug)

    payload = init_payload(f"Fiche commune : {commune.name}")
    payload["slug"] = slug
    payload["siren"] = commune.siren
    payload["commune_name"] = commune.name
    payload["data"] = commune_data(commune.siren)
    payload["page_data"] = {"type": "commune", "slug": slug}
    payload["page_summary"] = [
        {"link": "#donnees-contexte", "title": "Données de contexte"},
        {"link": "#intercommunalites-zonage", "title": "Intercommunalités et zonage"},
        {
            "link": "#ressources-financieres-fiscales",
            "title": "Ressources financières et fiscales",
        },
        {
            "link": "#comparaison-autres-communes",
            "title": "Comparaison avec d’autres communes",
        },
    ]
    payload["context"]["hide_brand"] = True
    return render(request, "core/commune_detail.html", payload)


@require_safe
def page_epci_detail(request, slug):
    epci = get_object_or_404(Epci, slug=slug)

    payload = init_payload(f"Fiche EPCI : {epci.name}")
    payload["slug"] = slug
    payload["siren"] = epci.siren
    payload["epci_name"] = epci.name
    payload["data"] = epci_data(epci.siren)
    payload["page_summary"] = [
        {"link": "#donnees-socio-economiques", "title": "Données socio-économiques"},
        {"link": "#coordonnees-siege", "title": "Coordonnées du siège"},
        {"link": "#perimetre-competences", "title": "Périmètre & compétences"},
        {
            "link": "#ressources-financieres-fiscales",
            "title": "Ressources financières et fiscales",
        },
        {"link": "#outils-pratiques", "title": "Outils pratiques"},
    ]
    tools = list_documents(document_type=3, publication_page=4, limit=10)
    payload["tools_list"] = documents_to_cards(tools)

    return render(request, "core/epci_detail.html", payload)


@require_safe
def page_departement_detail(request, slug):
    departement = get_object_or_404(Departement, slug=slug)

    payload = init_payload(f"Fiche département : {departement.name}")
    payload["slug"] = slug
    payload["siren"] = departement.siren
    payload["data"] = departement_data(departement)

    payload["page_summary"] = [
        {"link": "#donnees-contexte", "title": "Données de contexte"},
        {"link": "#perimetre", "title": "Périmètre"},
    ]

    return render(request, "core/departement_detail.html", payload)


@require_safe
def page_region_detail(request, slug):
    region = get_object_or_404(Region, slug=slug)

    payload = init_payload(f"Fiche région : {region.name}")
    payload["slug"] = slug
    payload["siren"] = region.siren
    payload["data"] = region_data(region)

    return render(request, "core/region_detail.html", payload)


##########################
# Place comparison pages #
##########################


@require_safe
def page_commune_compare(request, slug1, slug2, slug3=0, slug4=0):
    slugs = [slug1, slug2]
    sirens = []
    slugs_dict = {"slug1": slug1, "slug2": slug2}

    """
    Storing all supplementary slugs in slug2 because the reverse() function is not able to 
    figure out the optional slashes.
    """
    if slug3:
        slugs.append(slug3)
        slugs_dict["slug2"] = f"{slugs_dict['slug2']}/{slug3}"
    if slug4:
        slugs.append(slug4)
        slugs_dict["slug2"] = f"{slugs_dict['slug2']}/{slug4}"

    for s in slugs:
        commune = get_object_or_404(Commune, slug=s)
        sirens.append(commune.siren)

    payload = init_payload("Comparaison de communes")
    payload["data"] = {}
    payload["data"]["tables"] = communes_compare(sirens)

    payload["data"]["export_link"] = reverse(
        "core:csv_compare_communes_from_list", kwargs=slugs_dict
    )

    return render(request, "core/commune_compare.html", payload)


#####################
# Places list pages #
#####################


@require_safe
def page_region_liste_departements(request, slug):
    region = get_object_or_404(Region, slug=slug)
    departements = region.departement_set.all().order_by("name")
    payload = init_payload(
        f"Liste des { departements.count() } départements de la région {region.name}",
        links=[
            {
                "title": f"Fiche région : {region.name}",
                "url": reverse("core:page_region_detail", kwargs={"slug": region.slug}),
            }
        ],
    )
    payload["list"] = departements
    payload["entry_link"] = {
        "title": "Fiche département",
        "view": "core:page_departement_detail",
    }
    payload["subdivisions_link"] = {
        "title": "Liste des communes",
        "view": "core:page_departement_liste_communes",
    }
    return render(request, "core/place_list_direct_subdivisions.html", payload)


@require_safe
def page_region_liste_communes(request, slug):
    region = get_object_or_404(Region, slug=slug)
    departements = region.departement_set.all().order_by("name")
    all_communes_count = Commune.objects.filter(departement__region=region).count()
    payload = init_payload(
        f"Liste des { all_communes_count } communes de la région { region.name }",
        links=[
            {
                "title": f"Fiche région : { region.name }",
                "url": reverse("core:page_region_detail", kwargs={"slug": region.slug}),
            }
        ],
    )
    payload["sort_by_departement"] = True

    communes_by_departements = []
    for d in departements:
        communes = d.commune_set.all().order_by("name")
        communes_by_departements.append(
            {
                "title": f"Liste des { communes.count() } communes du département { d.name }",
                "list": communes,
            }
        )
    payload["list"] = communes_by_departements

    payload["entry_link"] = {
        "title": "Fiche commune",
        "view": "core:page_commune_detail",
    }
    return render(request, "core/place_list_direct_subdivisions.html", payload)


@require_safe
def page_region_liste_epcis(request, slug):
    region = get_object_or_404(Region, slug=slug)
    departements = region.departement_set.all().order_by("name")
    epcis_count = 0

    epcis_by_departements = []
    for d in departements:
        epcis = d.list_epcis()
        epcis_by_departements.append(
            {
                "title": f"Liste des { epcis.count() } EPCI du département { d.name }",
                "list": epcis,
            }
        )
        epcis_count += epcis.count()

    payload = init_payload(
        f"Liste des { epcis_count } EPCI de la région { region.name }",
        links=[
            {
                "title": f"Fiche région : { region.name }",
                "url": reverse("core:page_region_detail", kwargs={"slug": region.slug}),
            }
        ],
    )
    payload["sort_by_departement"] = True

    payload["list"] = epcis_by_departements

    payload["entry_link"] = {
        "title": "Fiche EPCI",
        "view": "core:page_epci_detail",
    }
    return render(request, "core/place_list_direct_subdivisions.html", payload)


@require_safe
def page_departement_liste_communes(request, slug):
    departement = get_object_or_404(Departement, slug=slug)
    communes = departement.commune_set.all().order_by("name")
    payload = init_payload(
        f"Liste des { communes.count() } communes du département {departement.name}",
        links=[
            {
                "title": f"Fiche département : {departement.name}",
                "url": reverse(
                    "core:page_departement_detail", kwargs={"slug": departement.slug}
                ),
            }
        ],
    )
    payload["list"] = communes
    payload["entry_link"] = {
        "title": "Fiche commune",
        "view": "core:page_commune_detail",
    }
    return render(request, "core/place_list_direct_subdivisions.html", payload)


@require_safe
def page_departement_liste_epcis(request, slug):
    departement = get_object_or_404(Departement, slug=slug)
    epcis = departement.list_epcis().order_by("slug")

    payload = init_payload(
        f"Liste des { len(epcis) } EPCI du département {departement.name}",
        links=[
            {
                "title": f"Fiche département : {departement.name}",
                "url": reverse(
                    "core:page_departement_detail", kwargs={"slug": departement.slug}
                ),
            }
        ],
    )
    payload["list"] = epcis
    payload["entry_link"] = {
        "title": "Fiche EPCI",
        "view": "core:page_epci_detail",
    }
    return render(request, "core/place_list_direct_subdivisions.html", payload)


###########################
# Documents related pages #
###########################


@require_safe
def page_publications(request):
    payload = init_payload("Publications")

    documents = list_documents(
        topic=request.GET.get("topic"),
        scope=request.GET.get("scope"),
        document_type=request.GET.get("document_type"),
        publication_page=request.GET.get("publication_page"),
        source_org=request.GET.get("source_org"),
        before=request.GET.get("before"),
        after=request.GET.get("after"),
    )

    cards = documents_to_cards(documents)

    paginated_docs = Paginator(cards, settings.PUBLICATIONS_PER_PAGE)

    data = {}
    data["total"] = paginated_docs.count
    data["cards_page"] = paginated_docs.get_page(request.GET.get("page"))

    payload["data"] = data

    payload["filters"] = publication_filters(request)

    return render(request, "core/publications.html", payload)


###############
# Legal pages #
###############


@require_safe
def page_accessibility(request):
    payload = init_payload("Déclaration d'accessibilité")
    return render(request, "core/accessibility.html", payload)


@require_safe
def page_legal(request):
    payload = init_payload("Mentions légales")
    return render(request, "core/mentions-legales.html", payload)


@require_safe
def page_sitemap(request):
    payload = init_payload("Plan du site")

    regions = Region.objects.order_by("name")
    regions_data = []
    for r in regions:
        regions_data.append(
            {"name": r.name, "slug": r.slug, "counts": r.subdivisions_count()}
        )

    filter_data = {}
    filter_data["topic"] = Topic.objects.order_by("name")
    filter_data["scope"] = Scope.objects.order_by("name")
    filter_data["source"] = Source.objects.order_by("title")
    payload["filter_data"] = filter_data

    payload["regions_data"] = regions_data

    return render(request, "core/sitemap.html", payload)


###############
# CSV exports #
###############
@require_safe
def csv_commune_export(request, slug):
    commune = Commune.objects.filter(slug=slug)
    # Commune.objects.filter is used instead of get_object_or_404 because
    # compare_communes_for_export expects a QuerySet
    filename = f"export-commune-{slug}"
    response = compare_communes_for_export(commune, filename)
    return response


@require_safe
def csv_compare_communes_from_list(request, slug1, slug2, slug3=0, slug4=0):
    slugs = [slug1, slug2]
    if slug3:
        slugs.append(slug3)
    if slug4:
        slugs.append(slug4)

    communes = Commune.objects.filter(slug__in=slugs)
    filename = f"comparaisons-communes-{'-'.join(slugs)}"

    response = compare_communes_for_export(communes, filename)
    return response


@require_safe
def csv_epci_compare_communes(request, slug):
    epci = get_object_or_404(Epci, slug=slug)
    filename = f"comparaisons-communes-{slug}"
    response = compare_communes_for_export(epci.commune_set.all(), filename)
    return response


@require_safe
def csv_departement_compare_communes(request, slug):
    departement = get_object_or_404(Departement, slug=slug)
    filename = f"comparaisons-communes-{slug}"
    response = compare_communes_for_export(departement.commune_set.all(), filename)
    return response


#############
# Test page #
#############


@require_safe
def page_tests(request):
    payload = init_payload("Tests")
    payload["breadcrumb_with_link"] = {
        "links": [{"url": "test-url", "title": "Test title"}],
        "current": "Test page",
    }
    payload["context"]["hide_brand"] = True
    return render(request, "core/tests.html", payload)
