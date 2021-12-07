from francedata.models import Region, Commune

from django.urls import reverse
from francedata.models.meta import DataYear

from collectivity_pages.services.context_data import ContextData


class RegionContextData(ContextData):
    base_model_name = "Region"
    data_model_name = "RegionData"
    data_model_key = "region"
    tables_page_type = "REG"


def region_data(region: Region, year: DataYear = None) -> dict:
    if not year:
        year = DataYear.objects.latest()

    response = {}

    response["name"] = region.name
    response["insee"] = region.insee
    response["siren"] = region.siren

    communes = Commune.objects.filter(departement__region=region)
    if communes.count() > 1:
        response["communes_list"] = {
            "name": f"Liste des {communes.count()} communes",
            "title": f"Liste des {communes.count()}  communes",
            "url": reverse(
                "core:page_region_liste_communes", kwargs={"slug": region.slug}
            ),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }
    elif communes.count() == 1:
        # Should be no case
        commune = communes[0]
        response["communes_list"] = {
            "name": commune.name,
            "title": f"Commune : { commune.name }",
            "url": reverse("core:page_commune_detail", kwargs={"slug": commune.slug}),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }

    epcis = communes.values("epci__slug", "epci__name").distinct()
    if epcis.count() > 1:
        response["epcis_list"] = {
            "name": f"Liste des {epcis.count()} EPCI",
            "title": f"Liste des {epcis.count()}  EPCI",
            "url": reverse(
                "core:page_region_liste_epcis", kwargs={"slug": region.slug}
            ),
            "image_path": "/static/img/hexagon2.svg",
            "svg_icon": True,
        }
    elif epcis.count() == 1:
        # Should be no case
        epci = epcis[0]
        response["epcis_list"] = {
            "name": epci["epci__name"],
            "title": f"EPCI : {epci['epci__name']}",
            "url": reverse(
                "core:page_epci_detail", kwargs={"slug": epci["epci__slug"]}
            ),
            "image_path": "/static/img/hexagon2.svg",
            "svg_icon": True,
        }

    departements = region.departement_set.all()
    if departements.count() > 1:
        response["departements_list"] = {
            "name": f"Liste des {departements.count()} departements",
            "title": f"Liste des {departements.count()} departements",
            "url": reverse(
                "core:page_region_liste_departements", kwargs={"slug": region.slug}
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }
    elif departements.count() == 1:
        # Should concern most DOMs
        departement = departements[0]
        response["departements_list"] = {
            "name": departement.name,
            "title": f"Département : { departement.name }",
            "url": reverse(
                "core:page_departement_detail", kwargs={"slug": departement.slug}
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }

    context_data = RegionContextData([region], datayear=year)
    context_data.fetch_collectivities_context_data()
    context_data.format_tables()

    return response
