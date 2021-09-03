from core.services.utils import init_payload
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from francedata.models import Epci

from core.services.epcis import epci_data

from core.services.publications import (
    list_documents,
    documents_to_cards,
)


@require_safe
def page_epci_detail(request, slug):
    epci = get_object_or_404(Epci, slug=slug)

    payload = init_payload(f"Données locales intercommunalité : {epci.name}")
    payload["slug"] = slug
    payload["siren"] = epci.siren
    payload["epci_name"] = epci.name
    payload["data"] = epci_data(epci.siren)
    payload["data"]["tables_header"] = ["Intitulé", "Donnée"]
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