#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from francedata.services.banatic import (
    import_commune_data_from_banatic,
    import_epci_data_from_banatic,
)
from django.core.management.base import BaseCommand

"""
Import de divers fichiers pour récupérer les données extraites de Banatic
- soit directement depuis le site web https://www.banatic.interieur.gouv.fr/
- soit depuis Datagouv https://www.data.gouv.fr/fr/datasets/base-nationale-sur-les-intercommunalites/

À rendre plus générique.

Ce script part du principe que les communes, départements et régions sont déjà importés
et doit donc être appelé après cog_import.py
"""


class Command(BaseCommand):
    help = "Import data from Banatic"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            type=str,
            help="If specified, only the current level will be parsed. \
                Caution: the script expects the previous levels to be already parsed",
            choices=["communes", "epci"],
        )
        parser.add_argument(
            "--year", type=int, help="If specified, only that year will be parsed"
        )

    def handle(self, *args, **options):
        message = "📥 Importing data from Banatic"

        if options["level"]:
            level = options["level"]
            all_levels = False
            message += f" for level {level}"
        else:
            level = None
            all_levels = True

        if options["year"]:
            year = int(options["year"])
            message += f" for year {year}"
        else:
            message += f" for the latest available year"
            year = 0

        print(message)
        # Now adding the Siren <-> Insee table for Communes first, then the epci and EPCI <=> communes relations

        # Import of the Siren <-> Insee table for Communes
        # That file also has population data
        if all_levels or level == "communes":
            import_commune_data_from_banatic(year)

        if all_levels or level == "epci":
            import_epci_data_from_banatic(year)
