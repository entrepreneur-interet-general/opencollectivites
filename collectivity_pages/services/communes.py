from django.db.models.query import QuerySet
from django.urls.base import reverse
from francedata.models.collectivity import Commune, CommuneData
from francedata.models.meta import DataYear
from collectivity_pages.services.context_data import ContextData
from collectivity_pages.services.utils import format_civility
from core.services.utils import generate_csv


class CommuneContextData(ContextData):
    base_model_name = "Commune"
    data_model_name = "CommuneData"
    data_model_key = "commune"
    tables_page_type = "COMM"


def commune_data(commune: Commune, year: DataYear = None):
    if not year:
        year = CommuneData.objects.latest("year__year").year
    # Get the basic data
    response = {
        item.datacode: item.value
        for item in CommuneData.objects.filter(commune=commune, year=year)
    }

    # Fix the 'civ_maire' syntax
    response["civ_maire"] = format_civility(response["civ_maire"])

    # Enrich the basic data
    ## Insee
    response["insee"] = commune.insee

    ## Code postal
    response["code_postal"] = response["CP"]

    ## Rank
    chef_lieu = response["chef_lieu"]
    if chef_lieu == "1":
        response["commune_type"] = "chef-lieu de canton"
    elif chef_lieu == "2":
        response["commune_type"] = "sous-préfecture"
    elif chef_lieu == "3":
        response["commune_type"] = "préfecture"
    elif chef_lieu == "4":
        response["commune_type"] = "préfecture de région"
    else:
        response["commune_type"] = ""

    # Subdivisions
    if not year:
        year = DataYear.objects.order_by("-year")[0]
    if commune.epci:
        response["epci"] = {
            "name": commune.epci.name,
            "title": f"EPCI : {commune.epci.name}",
            "url": reverse(
                "core:page_epci_detail",
                kwargs={"slug": commune.epci.slug},
            ),
            "image_path": "/static/img/hexagon2.svg",
            "svg_icon": True,
        }
    if commune.departement:
        response["departement"] = {
            "name": commune.departement.name,
            "title": f"Département : {commune.departement.name}",
            "url": reverse(
                "core:page_departement_detail",
                kwargs={"slug": commune.departement.slug},
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }
    if commune.departement.region and commune.departement.region.name != "Mayotte":
        response["region"] = {
            "name": commune.departement.region.name,
            "title": f"Région : {commune.departement.region.name}",
            "url": reverse(
                "core:page_region_detail",
                kwargs={"slug": commune.departement.region.slug},
            ),
            "image_path": "/static/img/hexagon4.svg",
            "svg_icon": True,
        }

    # Data Tables
    context_data = CommuneContextData([commune], datayear=year)
    context_data.fetch_collectivity_context_data(commune)
    context_data.format_tables()

    response["tables"] = context_data.formated_tables
    response["max_year"] = context_data.max_year

    return response


def communes_compare(communes: list, format_for_web: bool = True) -> dict:
    context_data = CommuneContextData(communes)
    context_data.fetch_collectivities_context_data()

    context_data.format_tables(format_for_web)

    return context_data.formated_tables


def compare_communes_for_export(qs: QuerySet, filename: str):
    communes_siren = list(qs.values_list("siren", flat=True))
    communes_insee = list(qs.values_list("insee", flat=True))

    members_context_data = communes_compare(qs, format_for_web=False)
    members_names = members_context_data.pop("places_names")

    title_row = ["Nom de la commune"] + members_names
    ids_table = [["SIREN"] + communes_siren, ["Insee"] + communes_insee]

    response = generate_csv(
        filename,
        title_row,
        table=ids_table,
        tables_dict=members_context_data,
    )

    return response
