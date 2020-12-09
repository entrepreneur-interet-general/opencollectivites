from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from aspic.models.t_aspic_communes import (
    T050Communes,
    T150DonneesCommunes,
    T052AdressesCommunes,
)
from aspic.models.t_aspic_cantons import T011Cantons
from aspic.serializers import T050CommunesSerializer, T150DonneesCommunesSerializer
from rest_framework.decorators import api_view
from django.db.models import Max


@api_view(["GET"])
def FicheCommuneView(request, siren):
    """
    Tous les champs nécessaires à la fiche commune
    """
    context = {"request": request}

    # get the basic data
    base_data = T050Communes.objects.get(siren=siren)
    base_serializer = T050CommunesSerializer(base_data, context=context)

    response = base_serializer.data

    # enrich the basic data
    response["insee"] = f"{response['dep']}{response['cod']}"

    # get the context data
    context_data = T150DonneesCommunes.objects.filter(siren=siren)
    most_recent = context_data.aggregate(Max("annee"))
    context_data_recent = context_data.filter(annee=most_recent["annee__max"])

    context_serializer = T150DonneesCommunesSerializer(
        context_data_recent, many=True, context=context
    )

    # reorder the context data
    for data in context_serializer.data:
        datacode = data["code_donnee"]
        value = data["valeur"]
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        response[datacode] = value

    # Missing data
    ## Code postal
    response["code_postal"] = T052AdressesCommunes.objects.get(siren=siren).code_postal

    ## Bassin de vie
    insee_bv = str(response["CodeBV"])

    dep = insee_bv[0:2]
    cod = insee_bv[2:5]

    response["NomBV"] = T050Communes.objects.get(dep=dep, cod=cod).nom

    return Response(response)


class CommuneBaseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = T050Communes.objects.all()
    serializer_class = T050CommunesSerializer
    lookup_field = "siren"
