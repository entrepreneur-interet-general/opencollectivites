from core.services.context_data import ContextData
from francedata.models import DataYear, Departement

from django.urls import reverse


class DepartementContextData(ContextData):
    aspic_data_model_name = "T109DonneesDepartements"
    fs_base_model_name = "Departement"
    context_properties = [
        {
            "field": "PopTot",
            "label": "Population totale en vigueur en {PopTot}",
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
            "label": "Variation annuelle moyenne de la population entre {TCAM} (en %)",
            "type": "numeric",
            "table": "population",
        },
        {
            "field": "PopActive1564",
            "label": "Taux d’activité des 15 à 64 ans en {PopActive1564%} (en %)",
            "type": "numeric",
            "table": "emploi",
        },
        {
            "field": "PopChom1564",
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
    ]

    def fetch_departements_context_data(self):
        for dept in self.list_collectivities():
            dept_number = dept.insee
            self.fetch_collectivity_context_data(
                dept.siren, "num_departement", dept_number
            )


def departement_data(dept_fs: Departement, year: DataYear = None) -> dict:
    if not year:
        year = DataYear.get_latest()

    response = {}

    response["name"] = dept_fs.name
    response["insee"] = dept_fs.insee
    response["siren"] = dept_fs.siren

    region = dept_fs.region
    response["region"] = {
        "name": region.name,
        "title": f"Région : {region.name}",
        "slug": region.slug,
        "url": reverse("core:page_region_detail", kwargs={"slug": region.slug}),
        "image_path": "/static/img/hexagon4.svg",
        "svg_icon": True,
    }

    communes = dept_fs.commune_set.all()
    communes_count = communes.count()
    if communes_count > 1:
        response["communes_list"] = {
            "name": f"Liste des {communes.count()} communes",
            "title": f"Liste des {communes.count()}  communes",
            "url": reverse(
                "core:page_departement_liste_communes", kwargs={"slug": dept_fs.slug}
            ),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }
    elif communes_count == 1:
        # Should only concern Paris
        commune = communes[0]
        response["communes_list"] = {
            "name": commune.name,
            "title": f"Commune : { commune.name }",
            "url": reverse("core:page_commune_detail", kwargs={"slug": commune.slug}),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }
    response["communes_count"] = communes_count

    epcis = dept_fs.list_epcis()
    if epcis.count() > 1:
        response["epcis_list"] = {
            "name": f"Liste des {epcis.count()} EPCI",
            "title": f"Liste des {epcis.count()}  EPCI",
            "url": reverse(
                "core:page_departement_liste_epcis", kwargs={"slug": dept_fs.slug}
            ),
            "image_path": "/static/img/hexagon2.svg",
            "svg_icon": True,
        }
    elif epcis.count() == 1:
        # Should only concern Paris
        epci = epcis[0]
        response["epcis_list"] = {
            "name": epci.name,
            "title": f"EPCI : {epci.name}",
            "url": reverse("core:page_epci_detail", kwargs={"slug": epci.slug}),
            "image_path": "/static/img/hexagon2.svg",
            "svg_icon": True,
        }

    dept_context_data = DepartementContextData([dept_fs], datayear=year)
    dept_context_data.fetch_departements_context_data()
    dept_context_data.format_tables()

    response["tables"] = dept_context_data.formated_tables
    response["max_year"] = dept_context_data.max_year

    return response
