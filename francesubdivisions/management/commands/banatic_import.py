#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import csv
from os import path
from pprint import pprint

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
