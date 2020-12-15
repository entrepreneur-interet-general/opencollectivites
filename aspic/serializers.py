from rest_framework import serializers
from aspic.models.t_aspic_communes import (
    T050Communes,
    T051Recensements,
    T150DonneesCommunes,
)
from aspic.models.t_aspic_cantons import T011Cantons

from aspic.models.t_aspic_other import T173DatesDonnees


class T050CommunesSerializer(serializers.ModelSerializer):
    class Meta:
        model = T050Communes
        depth = 2
        fields = [
            "siren",
            "num_departement",
            "dep",
            "cod",
            "nom",
            "ard",
            "can",
            "civ_maire",
            "pre_maire",
            "nom_maire",
        ]


class T150DonneesCommunesSerializer(serializers.ModelSerializer):
    class Meta:
        model = T150DonneesCommunes
        fields = ["siren", "code_donnee", "annee", "valeur"]
