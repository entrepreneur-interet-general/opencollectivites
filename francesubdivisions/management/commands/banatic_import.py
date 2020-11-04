#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from francesubdivisions.models import Epci, EpciType, Commune
import csv
from os import path
from pprint import pprint

YEAR = 2020

"""
Import de divers fichiers pour récupérer les données extraites de Banatic
- soit directement depuis le site web https://www.banatic.interieur.gouv.fr/
- soit depuis Datagouv https://www.data.gouv.fr/fr/datasets/base-nationale-sur-les-intercommunalites/

À rendre plus générique.

Ce script part du principe que les communes, départements et régions sont déjà importés
et doit donc être appelé après cog_import.py
"""


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Creation of the EPCI types if not already done
        """
        epci_types = [
            {"acronym": "CA", "name": "Communauté d'agglomération"},
            {"acronym": "CC", "name": "Communauté de communes"},
            {"acronym": "CU", "name": "Communauté urbaine"},
            {"acronym": "MET69", "name": "Métropole de Lyon"},
            {"acronym": "METRO", "name": "Métropole"},
        ]

        for et in epci_types:
            entry, return_code = EpciType.objects.get_or_create(
                acronym=et["acronym"], name=et["name"]
            )
        #"""

        # Import of the Siren <-> Insee table for Communes
        # That file also has population data
        """
        siren_insee_table = path.join("resources", "Banatic_SirenInsee2020.csv")
        with open(siren_insee_table, "r") as input_csv:
            reader = csv.DictReader(input_csv)
            for row in reader:
                name = row["nom_com"]
                insee = row["insee"]
                try:
                    commune = Commune.objects.get(year=YEAR, insee=insee)
                    if commune.name != name:
                        print(
                            f"Commune name {name} ({insee}) doesn't match with database entry {commune}"
                        )
                    commune.siren = row["siren"]
                    commune.population = row["ptot_2020"]
                    commune.save()
                except:
                    raise ValueError(f"Commune {name} ({insee}) not found")
        #"""

        # Import of the EPCI and member communes
        epci_member_list = path.join("resources", "perimetre_epci_france.csv")
        with open(epci_member_list, "r") as input_csv:
            reader = csv.DictReader(input_csv)
            for row in reader:
                epci_name = row["Nom du groupement"]
                epci_type = EpciType.objects.get(acronym=row["Nature juridique"])
                epci_siren = row["N° SIREN"]

                member_siren = row["Siren membre"]
                member_commune = Commune.objects.get(siren=member_siren, year=YEAR)

                epci_entry, return_code = Epci.objects.get_or_create(
                    name=epci_name, epci_type=epci_type, siren=epci_siren, year=YEAR
                )

                member_commune.epci = epci_entry
                member_commune.save()
