#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from francesubdivisions.models import Commune, Epci, Departement, Region
from francesubdivisions.models import validate_insee_commune
import csv
from os import path
from pprint import pprint
import re

"""
Ce script utilise l'archive "Ensemble" au format CSV telle que trouvée sur 
https://www.insee.fr/fr/information/2560452 :

- Choisir le millésime concerné et cliquer sur "Téléchargement des fichiers"
- Télécharger le fichier "Ensemble des fichiers <année> (csv)"
- le décompresser en tant que sous-répertoire d'un répertoire "resources" placé à la racine de Django
"""


class Command(BaseCommand):
    help = "Import data from the Code officiel géographique"

    def add_arguments(self, parser):
        parser.add_argument(
            "input_folder", nargs=1, type=str, help="The folder with the COG files"
        )
        parser.add_argument(
            "--level",
            type=str,
            help="If specified, only the current level will be parsed. \
                Caution: the script expects the previous levels to be already parsed",
        )

    def handle(self, *args, **options):
        if options["level"]:
            level = options["level"]
            all_levels = False
        else:
            level = None
            all_levels = True

        input_folder = options["input_folder"][0]
        input_path = path.join("resources", input_folder)
        year = int(re.findall(r"\d{4}", input_folder)[0])

        # Now going down from higher level: Régions, Départements, Communes

        # Régions
        if all_levels or level == "regions":
            regions_fullpath = path.join(input_path, f"region{year}.csv")
            regions = parse_file(regions_fullpath, "reg")

            for r in regions:
                entry, return_code = Region.objects.get_or_create(
                    name=r["name"], insee=r["insee"], year=year
                )
                if return_code:
                    print(f"Région {entry} created.")
                else:
                    print(f"Région {entry} already in database, skipped.")

        # Départements
        if all_levels or level == "departements":
            depts_fullpath = path.join(input_path, f"departement{year}.csv")
            depts = parse_file(depts_fullpath, "dep", "reg")

            for d in depts:
                region = Region.objects.get(year=year, insee=d["higher"])

                entry, return_code = Departement.objects.get_or_create(
                    name=d["name"], insee=d["insee"], year=year, region=region
                )
                if return_code:
                    print(f"Département {entry} created.")
                else:
                    print(f"Département {entry} already in database, skipped.")

        # Communes
        if all_levels or level == "communes":
            communes_fullpath = path.join(input_path, f"communes{year}.csv")
            communes = parse_file(communes_fullpath, "com", "dep", ("typecom", "COM"))

            for c in communes:
                dept = Departement.objects.get(year=year, insee=c["higher"])
                entry, return_code = Commune.objects.get_or_create(
                    name=c["name"], insee=c["insee"], year=year, departement=dept
                )
                if return_code:
                    print(f"Commune {entry} created.")
                else:
                    print(f"Commune {entry} already in database, skipped.")


def parse_file(input_file, insee_col, higher_col="", typecheck=False):
    """
    Parses one of the files from the COG.
    insee_col: the column with the relevant insee id for the current level
    higher_col: the column with the insee id of the immediate upper level (ex: département for commune)
    """
    with open(input_file, "r") as input_csv:
        reader = csv.DictReader(input_csv)
        entries = []
        if typecheck:
            tc_col = typecheck[0]
            tc_val = typecheck[1]

        for row in reader:
            if typecheck:
                if row[tc_col] != tc_val:
                    continue
            entry = {}
            entry["insee"] = row[insee_col]
            if higher_col:
                entry["higher"] = row[higher_col]
            entry["name"] = row["libelle"]
            entries.append(entry)
        return entries
