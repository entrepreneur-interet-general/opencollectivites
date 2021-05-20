from francesubdivisions.models import Departement

from django.urls import reverse


def departement_data(dept_fs: Departement) -> dict:
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
    if communes.count() > 1:
        response["communes_list"] = {
            "name": f"Liste des {communes.count()} communes",
            "title": f"Liste des {communes.count()}  communes",
            "url": reverse(
                "core:page_departement_liste_communes", kwargs={"slug": dept_fs.slug}
            ),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }
    elif communes.count() == 1:
        # Should only concern Paris
        commune = communes[0]
        response["communes_list"] = {
            "name": commune.name,
            "title": f"Commune : { commune.name }",
            "url": reverse("core:page_commune_detail", kwargs={"slug": commune.slug}),
            "image_path": "/static/img/hexagon1.svg",
            "svg_icon": True,
        }

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

    return response
