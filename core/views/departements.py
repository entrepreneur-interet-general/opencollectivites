from collectivity_pages.services.departements import departement_data
from collectivity_pages.services.utils import get_messages_for_collectivity
from core.services.publications import list_publications_for_collectivity
from core.services.utils import init_payload
from django.urls.base import reverse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from dsfr.utils import generate_summary_items
from francedata.models import Departement


@require_safe
def page_departement_detail(request, slug):
    departement = get_object_or_404(Departement, slug=slug)

    payload = init_payload(f"Données locales département : {departement.name}")
    payload["slug"] = slug
    payload["siren"] = departement.siren
    payload["data"] = departement_data(departement)
    payload["data"]["tables_header"] = ["Intitulé", "Donnée"]
    payload["page_menu"] = {
        "title": "Sommaire",
        "items": generate_summary_items(
            [
                "Données de contexte",
                "Ressources financières et fiscales",
                "Périmètre",
                "Études, statistiques et outils"
            ]
        ),
        "extra_classes": "fr-sidemenu--sticky-full-height fr-sidemenu--right",
    }

    payload["messages"] = get_messages_for_collectivity(
        collectivity_type="DEPT", collectivity_slug=slug
    )

    payload["publications"] = list_publications_for_collectivity(
        collectivity_type="departement", collectivity_slug=departement.slug
    )

    return render(request, "core/departement_detail.html", payload)


@require_safe
def page_departement_liste_communes(request, slug):
    departement = get_object_or_404(Departement, slug=slug)
    max_year = max(departement.commune_set.values_list("years", flat=True))
    communes = departement.commune_set.filter(years=max_year).order_by("name")
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
    max_year = max(departement.list_epcis().values_list("years", flat=True))
    epcis = departement.list_epcis().filter(years=max_year).order_by("slug")

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
