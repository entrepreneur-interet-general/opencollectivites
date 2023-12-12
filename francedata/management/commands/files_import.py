#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from francedata.models import DataSourceFile


class Command(BaseCommand):
    help = "Import data from the DataSourceFile files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--files", type=str, help="""
            If specified, the files with the specified ID will be imported,
            even if they are already marked as imported.
            Multiple file IDs must be separated by a comma
            """
        )


    def handle(self, *args, **options):
        # Manage output
        FORMAT = "%(asctime)s %(message)s"
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, format=FORMAT)

        force_files = options["files"]
        if force_files:
            files_to_import = [int(x) for x in force_files.split(',')]
            files = DataSourceFile.objects.filter(id__in=files_to_import)
        else:
            files = DataSourceFile.objects.filter(is_imported=False).order_by("created_at")

        if not files:
            logging.info("Pas de fichier à importer.")

        for file in files:
            logging.info(f"Import du fichier {file}.")
            response = file.import_file_data()
            result = response["success"]
            if result:
                file.mark_imported()
                logging.info("L’import a été effectué avec succès.")
            else:
                logging.error("Erreur lors de l’import.")
                for message in response["messages"]:
                    logging.error(message)
