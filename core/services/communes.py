from django.db.models import Max
from django.core import serializers

from .utils import format_number, data_vintage

from francesubdivisions.models import Commune, Epci, Departement, Region

from aspic.models.t_aspic_communes import (
    T050Communes,
    T150DonneesCommunes,
    T052AdressesCommunes,
)
from aspic.models.t_aspic_cantons import T011Cantons
from aspic.models.t_aspic_interco_liaison import T311050CommunesMembres
from aspic.models.t_aspic_interco_meta import T301NaturesJuridiques


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


def commune_context_data(siren_ids):
    """
    Renvoie les tableaux de données de contexte pour une liste de communes données
    """
    # Init the loop variables
    response = {}
    response["places_names"] = []
    context_data = {}
    max_year = None

    vintages = data_vintage()

    context_fields = [
        "PopTot",
        "PopMuni",
        "Densité",
        "TCAM",
        "PopActive1564%",
        "PopChom1564%",
        "RevenuFiscal",
        "ZRR",
        "ZUS",
        "Montagne",
        "Touristique",
        "DGF_Totale",
        "Forfaitaire",
        "DSU",
        "DSR",
        "DNP",
        "DGFParHab",
        "PopDGF",
        "DotationEluLocal",
        "SoldeFPIC",
        "AttributionFPIC",
        "ContributionFPIC",
        "SoldeFPIC_DGF",
    ]

    for siren_id in siren_ids:
        context_data[siren_id] = {}

        # list the places names
        response["places_names"].append(Commune.objects.get(siren=siren_id).name)

        context_data_unsorted = T150DonneesCommunes.objects.filter(siren=siren_id)

        # get the most recent year
        if not max_year:
            most_recent = context_data_unsorted.aggregate(Max("annee"))
            max_year = most_recent["annee__max"]
            response["max_year"] = max_year

        context_data_recent = context_data_unsorted.filter(annee=max_year)

        for data in context_data_recent:
            datacode = data.code_donnee
            value = data.valeur
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            context_data[siren_id][datacode] = value

        # make sure the keys exist
        for field in context_fields:
            if field not in context_data[siren_id]:
                context_data[siren_id][field] = ""

    # Prepare tables
    ## Population
    response["population"] = [
        [
            f"Population totale en vigueur en {vintages['PopTot']}",
        ],
        [
            f"Population municipale en vigueur en {vintages['PopMuni']}",
        ],
        [
            f"Densité démographique en {vintages['Densité']} (population totale/superficie géographique, en hab/km²)",
        ],
        [
            f"Variation annuelle de la population entre {vintages['TCAM']} (en %)",
        ],
    ]

    ## Emploi
    response["emploi"] = [
        [
            f"Taux d’activité des 15 à 64 ans en {vintages['PopActive1564%']} (en %)",
        ],
        [
            f"Taux de chômage des 15 à 64 ans en {vintages['PopChom1564%']} (en %)",
        ],
    ]

    ## Niveau de vie
    response["niveau_de_vie"] = [
        [
            f"Revenu fiscal médian des ménages par unité de consommation {vintages['RevenuFiscal']} (en €)",
        ],
    ]

    ## Zoning
    response["zonage"] = [
        [
            "Classement de la commune en zone de revitalisation rurale (ZRR)",
        ],
        [
            "Commune classée en zone urbaine sensible (ZUS)",
        ],
        [
            "Commune classée en zone de montagne",
        ],
        [
            "Commune classée comme touristique",
        ],
    ]

    ## Dotations
    response["dotation_globale"] = [
        [
            "Dotation globale de fonctionnement totale (en €)",
        ],
        [
            "Dont dotation forfaitaire (en €)",
        ],
        [
            " - dotation de solidarité urbaine et de cohésion sociale (DSU) (en €)",
        ],
        [
            " - dotation de solidarité rurale (DSR) (en €)",
        ],
        [
            " - dotation de péréquation totale (DNP) (en €)",
        ],
        [
            "DGF par habitant (en €)",
        ],
        ["Population « DGF »"],
    ]

    response["dotation_elu_local"] = [
        [
            "Dotation élu local (en €)",
        ],
    ]

    response["dotation_fpic"] = [
        [
            "Solde net FPIC (en €)",
        ],
        [
            "Dont reversement au profit de la commune (en €)",
        ],
        [
            "Dont prélèvement de la commune (en €)",
        ],
        [
            "FPIC par habitant (en €)",
        ],
    ]

    ################
    for siren_id in siren_ids:
        response["population"][0].append(
            format_number(context_data[siren_id]["PopTot"])
        )
        response["population"][1].append(
            format_number(context_data[siren_id]["PopMuni"])
        )
        response["population"][2].append(
            format_number(context_data[siren_id]["Densité"])
        )
        response["population"][3].append(format_number(context_data[siren_id]["TCAM"]))

        ## Emploi
        response["emploi"][0].append(
            format_number(context_data[siren_id]["PopActive1564%"])
        )
        response["emploi"][1].append(
            format_number(context_data[siren_id]["PopChom1564%"])
        )

        ## Niveau de vie
        response["niveau_de_vie"][0].append(
            format_number(context_data[siren_id]["RevenuFiscal"])
        )

        ## Zoning
        response["zonage"][0].append(
            "Classée en ZRR" if context_data[siren_id]["ZRR"] else "Non classée"
        )
        response["zonage"][1].append(
            "Classée en ZUS" if context_data[siren_id]["ZUS"] else "Non classée"
        )
        response["zonage"][2].append(
            "Classée" if context_data[siren_id]["Montagne"] else "Non classée"
        )
        response["zonage"][3].append(
            "Classée" if context_data[siren_id]["Touristique"] else "Non classée"
        )

        ## Dotations
        response["dotation_globale"][0].append(
            format_number(context_data[siren_id]["DGF_Totale"])
        )
        response["dotation_globale"][1].append(
            format_number(context_data[siren_id]["Forfaitaire"])
        )
        response["dotation_globale"][2].append(
            format_number(context_data[siren_id]["DSU"])
        )
        response["dotation_globale"][3].append(
            format_number(context_data[siren_id]["DSR"])
        )
        response["dotation_globale"][4].append(
            format_number(context_data[siren_id]["DNP"])
        )
        response["dotation_globale"][5].append(
            format_number(context_data[siren_id]["DGFParHab"])
        )
        response["dotation_globale"][6].append(
            format_number(context_data[siren_id]["PopDGF"])
        )

        response["dotation_elu_local"][0].append(
            format_number(context_data[siren_id]["DotationEluLocal"])
        )

        response["dotation_fpic"][0].append(
            format_number(context_data[siren_id]["SoldeFPIC"])
        )
        response["dotation_fpic"][1].append(
            format_number(context_data[siren_id]["AttributionFPIC"])
        )
        response["dotation_fpic"][2].append(
            format_number(context_data[siren_id]["ContributionFPIC"])
        )
        response["dotation_fpic"][3].append(
            format_number(context_data[siren_id]["SoldeFPIC_DGF"])
        )

    return response


def commune_data(siren_id):
    # Get the basic data
    response = T050Communes.objects.get(siren=siren_id).__dict__
    response.pop("_state", None)

    # Fix the 'civ_maire' syntax
    if response["civ_maire"] == "Mme":
        response["civ_maire"] = "M<sup>me</sup>"
    elif response["civ_maire"] == "M":
        response["civ_maire"] = "M."

    # Enrich the basic data
    ## Insee
    response["insee"] = f"{response['dep']}{response['cod']}"

    ## Code postal
    response["code_postal"] = T052AdressesCommunes.objects.get(
        siren=siren_id
    ).code_postal

    # Subdivisions
    subdivisions = Commune.objects.get(siren=siren_id)
    response["epci"] = {
        "name": subdivisions.epci.name,
        "title": f"EPCI : {subdivisions.epci.name}",
        "url": f"/epci/{subdivisions.epci.siren}/{subdivisions.epci.name}",
        "image_path": "/static/img/hexagon2.svg",
    }
    response["departement"] = {
        "name": subdivisions.departement.name,
        "title": f"Département : {subdivisions.departement.name}",
        "url": f"/departement/{subdivisions.departement.siren}/{subdivisions.departement.name}",
        "image_path": "/static/img/hexagon3.svg",
    }
    response["region"] = {
        "name": subdivisions.departement.region.name,
        "title": f"Région : {subdivisions.departement.region.name}",
        "url": f"/region/{subdivisions.departement.region.siren}/{subdivisions.departement.region.name}",
        "image_path": "/static/img/hexagon4.svg",
    }

    # Data Tables
    response["tables"] = commune_context_data([siren_id])
    response["max_year"] = response["tables"]["max_year"]

    ## Context_data

    ## Groups
    response["groupements"] = group_data(siren_id)

    return response