from django.urls.base import reverse
from core.services.utils import init_payload
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from francedata.models import Commune

from core.services.communes import (
    commune_data,
    communes_compare,
)


@require_safe
def page_commune_detail(request, slug):
    commune = get_object_or_404(Commune, slug=slug)

    payload = init_payload(f"Données locales commune : {commune.name}")
    payload["slug"] = slug
    payload["siren"] = commune.siren
    payload["commune_name"] = commune.name
    payload["data"] = commune_data(commune.siren)
    payload["page_data"] = {"type": "commune", "slug": slug}
    payload["data"]["tables_header"] = ["Intitulé", "Donnée"]
    payload["data"]["table_header_zonage"] = ["Intitulé", "Statut"]
    payload["data"]["table_header_interco"] = ["Type", "Nom", "Sigle type"]

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
    payload["data"]["tables_header"] = ["Intitulé"] + payload["data"]["tables"][
        "places_names"
    ]

    payload["data"]["export_link"] = reverse(
        "core:csv_compare_communes_from_list", kwargs=slugs_dict
    )

    return render(request, "core/commune_compare.html", payload)
