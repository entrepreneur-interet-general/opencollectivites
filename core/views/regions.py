from django.urls.base import reverse
from core.services.utils import init_payload
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from francedata.models import Commune, Region

from core.services.regions import region_data


@require_safe
def page_region_detail(request, slug):
    region = get_object_or_404(Region, slug=slug)

    payload = init_payload(f"Fiche région : {region.name}")
    payload["slug"] = slug
    payload["siren"] = region.siren
    payload["data"] = region_data(region)

    return render(request, "core/region_detail.html", payload)


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
def page_region_liste_departements(request, slug):
    region = get_object_or_404(Region, slug=slug)
    departements = region.departement_set.all().order_by("name")
    payload = init_payload(
        f"Liste des { departements.count() } départements de la région {region.name}",
        links=[
            {
                "title": f"Données locales région : {region.name}",
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
