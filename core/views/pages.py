from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .utils import init_payload, list_pages, publication_filters
from .communes import commune_data, commune_context_data
from .publications import list_documents, documents_to_cards
from pprint import pprint

########### Pages
def page_index(request):
    payload = init_payload()
    payload["title"] = "Accueil"
    return render(request, "core/index.html", payload)


def error404(request, exception):
    payload = init_payload()
    payload["title"] = "Erreur"
    payload["exception"] = exception
    return render(request, "core/404.html", payload)


def page_not_yet(request, siren, epci_name):
    payload = init_payload()
    payload["title"] = "Page en construction"
    return render(request, "core/page_not_yet.html", payload)


def page_commune_detail(request, siren, commune_name):
    payload = init_payload()
    payload["title"] = f"Fiche commune : {commune_name}"
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

    payload = init_payload()
    payload["data"] = {}
    payload["data"]["tables"] = commune_context_data(sirens)

    return render(request, "core/commune_compare.html", payload)


def page_publications(request):
    payload = init_payload()
    payload["title"] = "Publications"

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
    pprint(payload["filters"])

    return render(request, "core/publications.html", payload)


def page_tests(request):
    payload = init_payload()
    payload["title"] = "Tests"
    payload["context"]["hide_brand"] = True
    return render(request, "core/tests.html", payload)
