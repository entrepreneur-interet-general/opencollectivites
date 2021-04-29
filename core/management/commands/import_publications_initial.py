#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from datetime import datetime
from os import path
from urllib.parse import urlparse
import csv
import xlrd
from pprint import pprint
import requests
import bs4

from core.models import Source, Document, Scope

"""
Ce script importe les publications agrégées pendant la 
phase initiale de réflexion sur le défi OpenCollectivités
"""


class Command(BaseCommand):
    help = "Import data from the Code officiel géographique"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            type=str,
            help="If specified, only the current level will be parsed. \
                Caution: the script expects the previous levels to be already parsed",
            choices=["sources", "documents"],
        )

    def handle(self, *args, **options):
        if options["level"]:
            level = options["level"]
            all_levels = False
        else:
            level = None
            all_levels = True

        # Sources
        if all_levels or level == "sources":
            plateformes_file = path.join(
                "resources", "202101-sources-a-referencer_sources.csv"
            )
            with open(plateformes_file, "r", encoding="utf-8-sig") as input_csv:
                reader = csv.DictReader(input_csv)
                for row in reader:
                    url = row["URL"]
                    page_home = row["Page : Home"]
                    page_fiche_commune = row["Page : Fiche Commune"]
                    page_fiche_dept = row["Page : Fiche département"]
                    page_fiche_region = row["Page : fiche région"]
                    page_search_result = row["Page : résultat de recherche"]
                    type_coll = row["Filtre : type de collectivité"]
                    topics = row["Filtre : thématique"]
                    years = row["Millésimes"]
                    editors = row["Sources"]
                    doc_type = row["Type"]

                    last_update_excel = row["Date dernière màj"]
                    if last_update_excel:
                        last_update = datetime(
                            *xlrd.xldate_as_tuple(int(last_update_excel), 0)
                        )
                    else:
                        last_update = 0

                    entry = Source.objects.get_or_create(url=url)

                    hostname = urlparse(url).hostname

                    """
                    r = requests.get(url)
                    html = bs4.BeautifulSoup(r.text, features="html5lib")

                    if html.title:
                        title = html.title.text.replace("\r", "").replace("\n", "")
                    else:
                        title = ""
                    """

                    type_colls = type_coll.split(" ; ")
                    for tc in type_colls:
                        if tc:
                            tc_entry, return_code = Scope.objects.get_or_create(name=tc)

                            if return_code:
                                print(f"Scope {tc_entry} created.")
                            else:
                                print(f"Scope {tc_entry} already in database, skipped.")
