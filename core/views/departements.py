from core.services.departements import departement_data
from core.services.publications import list_publications_for_collectivity
from core.services.utils import init_payload
from django.urls.base import reverse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from francedata.models import Departement


@require_safe
def page_departement_detail(request, slug):
    departement = get_object_or_404(Departement, slug=slug)

    payload = init_payload(f"Données locales département : {departement.name}")
    payload["slug"] = slug
    payload["siren"] = departement.siren
    payload["data"] = departement_data(departement)
    payload["data"]["tables_header"] = ["Intitulé", "Donnée"]
    payload["page_summary"] = [
        {"link": "#donnees-contexte", "title": "Données de contexte"},
        {"link": "#perimetre", "title": "Périmètre"},
        {"link": "#list-publications", "title": "Études, statistiques et outils"},
    ]

    payload["publications"] = list_publications_for_collectivity(
        collectivity_type="departement", collectivity_id=departement.id
    )

    return render(request, "core/departement_detail.html", payload)


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
