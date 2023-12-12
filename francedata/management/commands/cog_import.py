#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from francedata.models import Departement, Region

from francedata.services.cog import (
    import_communes_from_cog,
    import_departements_from_cog,
    import_regions_from_cog,
)
from francedata.services.utils import add_sirens_and_categories

"""
Ce script récupère les données de
https://www.data.gouv.fr/fr/datasets/code-officiel-geographique-cog/
pour les régions, départements et communes à partir de 2019

D'après https://www.insee.fr/fr/information/2560452:
"Depuis le millésime 2019, les fichiers ont sensiblement évolué 
dans leur format et leur structure."
"""


class Command(BaseCommand):
    help = "Import data from the Code officiel géographique"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            type=str,
            help="If specified, only the current level will be parsed. \
                Caution: the script expects the previous levels to be already parsed",
            choices=["regions", "departements", "communes"],
        )
        parser.add_argument(
            "--year", type=int, help="If specified, only that year will be parsed"
        )

    def handle(self, *args, **options):
        if options["level"]:
            level = options["level"]
            all_levels = False
        else:
            level = None
            all_levels = True

        if options["year"]:
            year = int(options["year"])
        else:
            year = 0

        # Now going down from higher level: Régions, Départements, Communes

        # Régions
        if all_levels or level == "regions":
            # First import data from the COG
            response = import_regions_from_cog(year)

            # Then the SIRENs from a local file
            regions_list = "regions-siren.csv"
            add_sirens_and_categories(regions_list, Region, response["year_entry"])

        # Départements
        if all_levels or level == "departements":
            # First import data from the COG
            response = import_departements_from_cog(year)

            # Then the SIRENs from a local file
            depts_list = "departements-siren.csv"
            add_sirens_and_categories(depts_list, Departement, response["year_entry"])

        # Communes
        if all_levels or level == "communes":
            response = import_communes_from_cog(year)
