from collectivity_pages.services.context_data import ContextData
from francedata.models.meta import DataYear
from francedata.models.collectivity import Departement
from django.urls.base import reverse


class DepartementContextData(ContextData):
    base_model_name = "Departement"
    data_model_name = "DepartementData"
    data_model_key = "departement"
    tables_page_type = "DEPT"


def departement_data(dept: Departement, year: DataYear = None) -> dict:
    if not year:
        year = DataYear.objects.latest()

    response = {}

    response["name"] = dept.name
    response["insee"] = dept.insee
    response["siren"] = dept.siren

    if dept.region:
        region = dept.region
        response["region"] = {
            "name": region.name,
            "title": f"Région : {region.name}",
            "slug": region.slug,
            "url": reverse("core:page_region_detail", kwargs={"slug": region.slug}),
            "image_path": "/static/img/hexagon4.svg",
            "svg_icon": True,
        }

    max_year = max(dept.commune_set.values_list("years", flat=True))
    communes = dept.commune_set.filter(years=max_year)
    communes_count = communes.count()
    if communes_count > 1:
        response["communes_list"] = {
            "name": f"Liste des {communes.count()} communes",
            "title": f"Liste des {communes.count()}  communes",
            "url": reverse(
                "core:page_departement_liste_communes", kwargs={"slug": dept.slug}
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

    epcis = dept.list_epcis()
    if epcis.count() > 1:
        response["epcis_list"] = {
            "name": f"Liste des {epcis.count()} EPCI",
            "title": f"Liste des {epcis.count()}  EPCI",
            "url": reverse(
                "core:page_departement_liste_epcis", kwargs={"slug": dept.slug}
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

    dept_context_data = DepartementContextData([dept], datayear=year)
    dept_context_data.fetch_collectivities_context_data()
    dept_context_data.format_tables()

    response["tables"] = dept_context_data.formated_tables
    response["max_year"] = dept_context_data.max_year

    return response
