from core.services.utils import generate_csv
from django.db.models.query import QuerySet
from django.urls.base import reverse
from .context_data import ContextData

from francedata.models import Commune, DataYear

from aspic.models.t_aspic_communes import (
    T050Communes,
    T052AdressesCommunes,
)

from aspic.models.t_aspic_interco_liaison import T311050CommunesMembres
from aspic.models.t_aspic_interco_meta import T301NaturesJuridiques

from aspic.utils import clean_civility


class CommuneContextData(ContextData):
    aspic_data_model_name = "T150DonneesCommunes"
    fs_base_model_name = "Commune"
    context_properties = [
        {
            "field": "PopTot",
            "label": "Population totale en vigueur en {PopTot}",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "PopMuni",
            "label": "Population municipale en vigueur en {PopMuni}",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "Densité",
            "label": "Densité démographique en {Densité} (population totale/superficie géographique, en hab/km²)",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "TCAM",
            "label": "Variation annuelle de la population entre {TCAM} (en %)",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "PopActive1564%",
            "label": "Taux d’activité des 15 à 64 ans en {PopActive1564%} (en %)",
            "type": "numeric",
            "table": "emploi",
        },
        {
            "field": "PopChom1564%",
            "label": "Taux de chômage des 15 à 64 ans en {PopChom1564%} (en %)",
            "type": "numeric",
            "table": "emploi",
        },
        {
            "field": "RevenuFiscal",
            "label": "Revenu fiscal médian des ménages par unité de consommation {RevenuFiscal} (en €)",
            "type": "numeric",
            "table": "niveau_de_vie",
        },
        {
            "field": "ZRR",
            "label": "Classement de la commune en zone de revitalisation rurale (ZRR)",
            "type": "boolean",
            "value_true": "Classée en ZRR",
            "value_false": "Non classée",
            "table": "zonage",
        },
        {
            "field": "ZUS",
            "label": "Commune classée en zone urbaine sensible (ZUS)",
            "type": "boolean",
            "value_true": "Classée en ZUS",
            "value_false": "Non classée",
            "table": "zonage",
        },
        {
            "field": "Montagne",
            "label": "Commune classée en zone de montagne",
            "type": "boolean",
            "value_true": "Classée",
            "value_false": "Non classée",
            "table": "zonage",
        },
        {
            "field": "Touristique",
            "label": "Commune classée comme touristique",
            "type": "boolean",
            "value_true": "Classée",
            "value_false": "Non classée",
            "table": "zonage",
        },
        {
            "field": "DGF_Totale",
            "label": "Dotation globale de fonctionnement totale (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "Forfaitaire",
            "label": "Dont dotation forfaitaire (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DSU",
            "label": " - dotation de solidarité urbaine et de cohésion sociale (DSU) (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DSR",
            "label": " - dotation de solidarité rurale (DSR) (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DNP",
            "label": " - dotation de péréquation totale (DNP) (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DGFParHab",
            "label": "DGF par habitant (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "PopDGF",
            "label": "Population « DGF »",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DotationEluLocal",
            "label": "Dotation élu local (en €)",
            "type": "numeric",
            "table": "dotation_elu_local",
        },
        {
            "field": "SoldeFPIC",
            "label": "Solde net FPIC (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
        {
            "field": "AttributionFPIC",
            "label": "Dont reversement au profit de la commune (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
        {
            "field": "ContributionFPIC",
            "label": "Dont prélèvement de la commune (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
        {
            "field": "SoldeFPIC_DGF",
            "label": "FPIC par habitant (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
    ]


def group_data(siren_id):
    """
    Renvoie les groupements auxquels appartient une commune
    """
    response = []

    group_types = T301NaturesJuridiques.objects.order_by("ordre_affichage")

    groups = (
        T311050CommunesMembres.objects.filter(membre=siren_id)
        .filter(groupement__archive=False)
        .values(
            "groupement__raison_sociale",
            "groupement__nature_juridique",
            "groupement_id",
        )
    )

    for gt in group_types:
        for group in groups:
            if gt.code == group["groupement__nature_juridique"]:
                response.append(
                    [
                        gt.libelle,
                        f"{group['groupement__raison_sociale']} ({group['groupement_id']})",
                        gt.code,
                    ]
                )
    return response


def commune_data(siren_id: str, year: DataYear = None):
    # Get the basic data
    response = T050Communes.objects.get(siren=siren_id).__dict__
    response.pop("_state", None)

    # Fix the 'civ_maire' syntax
    response["civ_maire"] = clean_civility(response["civ_maire"])

    # Enrich the basic data
    ## Insee
    response["insee"] = f"{response['dep']}{response['cod']}"

    ## Code postal
    response["code_postal"] = T052AdressesCommunes.objects.get(
        siren=siren_id
    ).code_postal

    # Subdivisions
    if not year:
        year = DataYear.objects.order_by("-year")[0]
    subdivisions = Commune.objects.get(siren=siren_id, years=year)
    if subdivisions.epci:
        response["epci"] = {
            "name": subdivisions.epci.name,
            "title": f"EPCI : {subdivisions.epci.name}",
            "url": reverse(
                "core:page_epci_detail",
                kwargs={"slug": subdivisions.epci.slug},
            ),
            "image_path": "/static/img/hexagon2.svg",
            "svg_icon": True,
        }
    if subdivisions.departement:
        response["departement"] = {
            "name": subdivisions.departement.name,
            "title": f"Département : {subdivisions.departement.name}",
            "url": reverse(
                "core:page_departement_detail",
                kwargs={"slug": subdivisions.departement.slug},
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }
    if (
        subdivisions.departement.region
        and subdivisions.departement.region.name != "Mayotte"
    ):
        response["region"] = {
            "name": subdivisions.departement.region.name,
            "title": f"Région : {subdivisions.departement.region.name}",
            "url": reverse(
                "core:page_region_detail",
                kwargs={"slug": subdivisions.departement.region.slug},
            ),
            "image_path": "/static/img/hexagon4.svg",
            "svg_icon": True,
        }

    # Data Tables
    context_data = CommuneContextData([siren_id], datayear=year)
    context_data.fetch_collectivity_context_data(siren_id)
    context_data.format_tables()

    response["tables"] = context_data.formated_tables
    response["max_year"] = context_data.max_year

    ## Groups
    response["groupements"] = group_data(siren_id)

    return response


def communes_compare(sirens: list, format_for_web: bool = True) -> dict:
    context_data = CommuneContextData(sirens)
    context_data.fetch_collectivities_context_data()

    context_data.format_tables(format_for_web)

    return context_data.formated_tables


def compare_communes_for_export(qs: QuerySet, filename: str):
    communes_siren = list(qs.values_list("siren", flat=True))
    communes_insee = list(qs.values_list("insee", flat=True))

    members_context_data = communes_compare(communes_siren, format_for_web=False)
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
