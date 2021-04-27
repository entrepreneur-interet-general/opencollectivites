from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from core.models import Topic, Scope, Source
from core.services.utils import init_payload, list_pages, publication_filters
from core.services.communes import commune_data, commune_context_data
from core.services.publications import list_documents, documents_to_cards

from francesubdivisions.models import Region

from pprint import pprint

########### Pages
def page_index(request):
    payload = init_payload("Accueil")
    return render(request, "core/index.html", payload)


def error404(request, exception):
    payload = init_payload("Erreur")
    payload["exception"] = exception
    return render(request, "core/404.html", payload)


def page_not_yet(request, **kwargs):
    payload = init_payload("Page en construction")
    return render(request, "core/page_not_yet.html", payload)


def page_commune_detail(request, siren, commune_name):
    payload = init_payload(f"Fiche commune : {commune_name}")
    payload["siren"] = siren
    payload["commune_name"] = commune_name
    payload["data"] = commune_data(siren)
    payload["page_data"] = {"type": "commune", "siren": siren}
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


def page_commune_compare(request, siren1, siren2, siren3=0, siren4=0):
    sirens = [siren1, siren2]

    if siren3:
        sirens.append(siren3)
    if siren4:
        sirens.append(siren4)

    payload = init_payload("Comparaison de communes")
    payload["data"] = {}
    payload["data"]["tables"] = commune_context_data(sirens)

    return render(request, "core/commune_compare.html", payload)


def page_publications(request):
    payload = init_payload("Publications")

    documents = list_documents(
        topic=request.GET.get("topic"),
        scope=request.GET.get("scope"),
        document_type=request.GET.get("document_type"),
        publication_page=request.GET.get("publication_page"),
    )

    cards = documents_to_cards(documents)

    paginated_docs = Paginator(cards, settings.PUBLICATIONS_PER_PAGE)

    data = {}
    data["total"] = paginated_docs.count
    data["cards_page"] = paginated_docs.get_page(request.GET.get("page"))

    payload["data"] = data

    payload["filters"] = publication_filters(request)

    return render(request, "core/publications.html", payload)


def page_legal(request):
    payload = init_payload("Mentions légales")
    return render(request, "core/mentions-legales.html", payload)


def page_sitemap(request):
    payload = init_payload("Plan du site")

    regions = Region.objects.order_by("name")
    regions_data = []
    for r in regions:
        # Using insee because Mayotte should appear here
        regions_data.append(
            {"name": r.name, "slug": r.slug, "counts": r.subdivisions_count()}
        )

    filter_data = {}
    filter_data["topic"] = Topic.objects.order_by("name")
    filter_data["scope"] = Scope.objects.order_by("name")
    filter_data["source"] = Source.objects.order_by("title")
    payload["filter_data"] = filter_data

    pprint(regions_data)
    payload["regions_data"] = regions_data

    return render(request, "core/sitemap.html", payload)


def page_tests(request):
    payload = init_payload("Tests")
    payload["context"]["hide_brand"] = True
    return render(request, "core/tests.html", payload)
