from francedata.models import Region, Commune

from django.urls import reverse


def region_data(region_fs: Region) -> dict:
    response = {}

    response["name"] = region_fs.name
    response["insee"] = region_fs.insee
    response["siren"] = region_fs.siren

    communes = Commune.objects.filter(departement__region=region_fs)
    if communes.count() > 1:
        response["communes_list"] = {
            "name": f"Liste des {communes.count()} communes",
            "title": f"Liste des {communes.count()}  communes",
            "url": reverse(
                "core:page_region_liste_communes", kwargs={"slug": region_fs.slug}
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
                "core:page_region_liste_epcis", kwargs={"slug": region_fs.slug}
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

    departements = region_fs.departement_set.all()
    if departements.count() > 1:
        response["departements_list"] = {
            "name": f"Liste des {departements.count()} departements",
            "title": f"Liste des {departements.count()} departements",
            "url": reverse(
                "core:page_region_liste_departements", kwargs={"slug": region_fs.slug}
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }
    elif departements.count() == 1:
        # Should concern most DOMs
        departement = departements[0]
        response["departements_list"] = {
            "name": departement.name,
            "title": f"Commune : { departement.name }",
            "url": reverse(
                "core:page_departement_detail", kwargs={"slug": departement.slug}
            ),
            "image_path": "/static/img/hexagon3.svg",
            "svg_icon": True,
        }

    return response
