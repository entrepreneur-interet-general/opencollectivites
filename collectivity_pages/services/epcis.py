from collectivity_pages.services.context_data import ContextData
from francedata.models.meta import DataYear
from francedata.models.collectivity import Commune, Epci, EpciData
from django.urls.base import reverse


class EpciContextData(ContextData):
    base_model_name = "Epci"
    data_model_name = "EpciData"
    data_model_key = "epci"
    tables_page_type = "EPCI"


def epci_data(siren_id, year: DataYear = None):
    # Get the basic data
    epci = Epci.objects.get(siren=siren_id)

    if not year:
        year = EpciData.objects.latest("year__year").year
    # Get the basic data
    response = {
        item.datacode: item.value
        for item in EpciData.objects.filter(epci=epci).order_by("year__year")
    }

    response["siren"] = epci.siren
    response["name"] = epci.name

    response["type"] = {
        "name": epci.get_epci_type_display(),
        "acronym": epci.epci_type,
    }

    """
    response["contact"] = {}
    response["contact"]["address1"] = epci_aspic.ligne_1
    response["contact"]["address2"] = epci_aspic.ligne_2
    response["contact"]["address3"] = epci_aspic.ligne_3
    response["contact"]["postcode"] = epci_aspic.code_postal
    response["contact"]["city"] = epci_aspic.commune_siege.nom
    response["contact"]["telephone"] = epci_aspic.telephone
    response["contact"]["fax"] = epci_aspic.fax
    response["contact"]["email"] = epci_aspic.adresse_e_mail
    response["contact"]["website"] = epci_aspic.sanitize_website()
    """

    # Navigation cards
    if "commune_siege_id" in response:
        seat = Commune.objects.get(siren=response["commune_siege_id"])

        response["seat"] = {
            "name": seat.name,
            "title": f"Siège : {seat.name}",
            "slug": seat.slug,
            "url": reverse(
                "core:page_commune_detail",
                kwargs={"slug": seat.slug},
            ),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }
        response["departement"] = {
            "name": seat.departement.name,
            "title": f"Département du siège : {seat.departement.name}",
            "slug": seat.departement.slug,
            "url": reverse(
                "core:page_departement_detail",
                kwargs={"slug": seat.departement.slug},
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }

        if seat.departement.region.name != "Mayotte":
            # Mayotte is not a proper region
            response["regions"] = (
                epci.commune_set.all()
                .values("departement__region__slug", "departement__region__name")
                .distinct()
            )

            response["region"] = {
                "name": seat.departement.region.name,
                "title": f"Région du siège : {seat.departement.region.name}",
                "slug": seat.departement.region.slug,
                "url": reverse(
                    "core:page_region_detail",
                    kwargs={"slug": seat.departement.region.slug},
                ),
                "image_path": "/static/img/hexagon4.svg",
                "svg_icon": True,
            }

    max_year = max(epci.commune_set.values_list("years", flat=True))
    response["departements"] = (
        epci.commune_set.filter(years=max_year)
        .values(
            "departement__slug",
            "departement__name",
            "departement__region__slug",
            "departement__region__name",
        )
        .distinct()
    )

    response["communes_list"] = {
        "name": "Liste des communes",
        "title": "Liste des communes",
        "url": "#perimetre",
        "image_path": "/static/img/hexagon1.svg",
        "svg_icon": True,
    }

    response["members"] = epci.commune_set.filter(years=max_year).order_by("name")

    epci_context_data = EpciContextData([epci])
    epci_context_data.fetch_collectivities_context_data()
    epci_context_data.format_tables()

    response["tables"] = epci_context_data.formated_tables
    response["max_year"] = epci_context_data.max_year

    return response
