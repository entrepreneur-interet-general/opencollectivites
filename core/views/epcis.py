from core.services.utils import init_payload
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from dsfr.utils import generate_summary_items
from francedata.models import Epci

from core.services.epcis import epci_data

from core.services.publications import (
    list_documents,
    documents_to_cards,
    list_publications_for_collectivity,
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

    payload["page_menu"] = {
        "title": "Sommaire",
        "items": generate_summary_items(
            [
                "Données socio-économiques",
                "Coordonnées du siège",
                "Périmètre & compétences",
                "Ressources financières et fiscales",
                "Études, statistiques et outils",
            ]
        ),
        "extra_classes": "fr-sidemenu--sticky-full-height fr-sidemenu--right",
    }

    tools = list_documents(document_type=3, publication_page=4, limit=10)
    payload["tools_list"] = documents_to_cards(tools)

    payload["publications"] = list_publications_for_collectivity(
        collectivity_type="epci", collectivity_id=epci.id
    )

    return render(request, "core/epci_detail.html", payload)
