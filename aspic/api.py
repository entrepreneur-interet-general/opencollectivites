from ninja import Router
from aspic.models.t_aspic_communes import (
    T050Communes,
    T150DonneesCommunes,
    T052AdressesCommunes,
)
from aspic.models.t_aspic_cantons import T011Cantons
from aspic.models.t_aspic_interco_liaison import T311050CommunesMembres
from aspic.models.t_aspic_other import T173DatesDonnees
from django.db.models import Max
from django.core import serializers

router = Router()


@router.get("/fiche-commune/{siren_id}", tags=["aspic"])
def get_fiche_commune(request, siren_id):
    """
    Tous les champs nécessaires à la fiche commune
    """

    response = T050Communes.objects.get(siren=siren_id).__dict__
    response.pop("_state", None)

    # enrich the basic data
    response["insee"] = f"{response['dep']}{response['cod']}"

    # get the context data
    context_data = T150DonneesCommunes.objects.filter(siren=siren_id)
    most_recent = context_data.aggregate(Max("annee"))
    context_data_recent = context_data.filter(annee=most_recent["annee__max"])

    response["T150"] = {}
    response["T150"]["max_year"] = most_recent["annee__max"]
    # reorder the context data
    for data in context_data_recent:
        datacode = data.code_donnee
        value = data.valeur
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        response["T150"][datacode] = value

    # get the year of the data
    years = {}

    years_data = T173DatesDonnees.objects.all()
    for y in years_data:
        years[y.code] = y.libelle

    response["years"] = years

    # Missing data
    ## Code postal
    response["code_postal"] = T052AdressesCommunes.objects.get(
        siren=siren_id
    ).code_postal

    ## Groupements
    response["groupements"] = list(
        T311050CommunesMembres.objects.filter(membre=siren_id)
        .filter(groupement__archive=False)
        .values(
            "groupement__raison_sociale",
            "groupement__nature_juridique",
            "groupement_id",
        )
    )
    # """

    return response