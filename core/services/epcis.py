from django.urls.base import reverse
from francedata.models import Epci, Commune
from aspic.models.t_aspic_intercommunalites import (
    T311Groupements,
    T311DeleguesCom,
    T172PopGroupements,
)
from aspic.models.t_aspic_interco_liaison import T302311CompetencesGroup

from aspic.utils import clean_civility
from .context_data import ContextData


class EpciContextData(ContextData):
    context_properties = [
        {
            "field": "population",
            "label": "Population totale regroupée",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "pop_density",
            "label": "Densité de population (hab/km²)",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "DGF_Totale",
            "label": "Dotation globale de fonctionnement totale de fonctionnement (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "Dotation_Interco",
            "label": " - dont dotation d’intercommunalité",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "Dotation_Compensation",
            "label": " - dont dotation de compensation",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DgfTotaleParHab",
            "label": "DGF totale par habitant (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "DgfIntercoParHab",
            "label": "Dotation d’intercommunalité par habitant (en €)",
            "type": "numeric",
            "table": "dotation_globale",
        },
        {
            "field": "FPIC_Solde",
            "label": "Solde de l’ensemble intercommunal (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
        {
            "field": "FPIC_Prélèvement",
            "label": " - dont prélèvement de l’ensemble intercommunal (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
        {
            "field": "FPIC_Reversement",
            "label": " - dont versement au profit de l’ensemble intercommunal (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
        {
            "field": "FPICParHab",
            "label": "FPIC par habitant (en €)",
            "type": "numeric",
            "table": "dotation_fpic",
        },
    ]
    aspic_data_model_name = "T171DonneesGroupements"
    fs_base_model_name = "Epci"

    def fetch_epcis_context_data(self):
        for siren_id in self.list_sirens():

            self.fetch_collectivity_context_data(siren_id)
            # Get additional context data
            try:
                pop_data = T172PopGroupements.objects.get(siren=siren_id)
            except T172PopGroupements.DoesNotExist:
                pop_data = None

            if pop_data:
                self.context_data[siren_id]["population"] = pop_data.pop_tot
                self.context_data[siren_id]["pop_density"] = (
                    pop_data.pop_tot / pop_data.superficie * 100
                )


def epci_data(siren_id):
    # Get the basic data
    epci_fs = Epci.objects.get(siren=siren_id)
    epci_aspic = T311Groupements.objects.get(siren=siren_id)
    response = {}

    response["siren"] = epci_aspic.siren
    response["name"] = epci_aspic.raison_sociale

    response["president"] = get_epci_president(epci_aspic)

    response["type"] = {
        "name": epci_fs.get_epci_type_display(),
        "acronym": epci_fs.epci_type,
    }

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

    # Navigation cards
    seat = Commune.objects.get(siren=epci_aspic.commune_siege_id)

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

    response["departements"] = (
        epci_fs.commune_set.all()
        .values("departement__slug", "departement__name")
        .distinct()
    )

    if seat.departement.region.name != "Mayotte":
        # Mayotte is not a proper region
        response["regions"] = (
            epci_fs.commune_set.all()
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

    response["communes_list"] = {
        "name": "Liste des communes",
        "title": "Liste des communes",
        "url": "#perimetre",
        "image_path": "/static/img/hexagon1.svg",
        "svg_icon": True,
    }

    response["members"] = epci_fs.commune_set.all().order_by("name")

    response["competences"] = T302311CompetencesGroup.objects.filter(
        groupement=epci_aspic
    )

    epci_context_data = EpciContextData([siren_id])
    epci_context_data.fetch_epcis_context_data()
    epci_context_data.format_tables()

    response["tables"] = epci_context_data.formated_tables
    response["max_year"] = epci_context_data.max_year

    return response


def get_epci_president(entity):
    president = T311DeleguesCom.objects.get(groupement=entity, fonction="Président")

    response = {}
    response["civility"] = clean_civility(president.civilite)
    response["first_name"] = president.prenom
    response["last_name"] = president.nom
    return response
