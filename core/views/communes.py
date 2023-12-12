from collectivity_pages.services.utils import get_messages_for_collectivity
from core.services.publications import list_publications_for_collectivity
from django.urls.base import reverse
from core.services.utils import init_payload
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from francedata.models import Commune

from collectivity_pages.services.communes import commune_data, communes_compare

from dsfr.utils import generate_summary_items


@require_safe
def page_commune_detail(request, slug):
    commune = get_object_or_404(Commune, slug=slug)

    payload = init_payload(f"Données locales commune : {commune.name}")
    payload["slug"] = slug
    payload["siren"] = commune.siren
    payload["commune_name"] = commune.name
    payload["data"] = commune_data(commune)
    payload["page_data"] = {"type": "commune", "slug": slug}
    payload["data"]["tables_header"] = ["Intitulé", "Donnée"]
    payload["data"]["table_header_zonage"] = ["Intitulé", "Statut"]
    payload["data"]["table_header_interco"] = ["Type", "Nom", "Sigle type"]

    payload["page_menu"] = {
        "title": "Sommaire",
        "items": generate_summary_items(
            [
                "Données de contexte",
                "Intercommunalités et zonage",
                "Ressources financières et fiscales",
                "Comparaison avec d’autres communes",
                "Études, statistiques et outils",
            ]
        ),
        "extra_classes": "fr-sidemenu--sticky-full-height fr-sidemenu--right",
    }

    payload["messages"] = get_messages_for_collectivity(
        collectivity_type="COMM", collectivity_slug=slug
    )

    payload["publications"] = list_publications_for_collectivity(
        collectivity_type="commune", collectivity_slug=commune.slug
    )

    payload["context"]["hide_brand"] = False
    return render(request, "core/commune_detail.html", payload)


@require_safe
def page_commune_compare(request, slug1, slug2, slug3=0, slug4=0):
    slugs = [slug1, slug2]
    communes = []
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
        communes.append(commune)

    payload = init_payload("Comparaison de communes")
    payload["data"] = {}
    payload["data"]["tables"] = communes_compare(communes)
    payload["data"]["tables_header"] = ["Intitulé"] + payload["data"]["tables"][
        "places_names"
    ]

    payload["data"]["export_link"] = reverse(
        "core:csv_compare_communes_from_list", kwargs=slugs_dict
    )

    return render(request, "core/commune_compare.html", payload)
