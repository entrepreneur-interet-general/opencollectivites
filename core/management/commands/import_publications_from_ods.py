#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from dateutil import parser as dateparser
from external_apis.models import OpenDataSoftQuery


class Command(BaseCommand):
    help = "Import publications from OpenDataSoft projects."

    def add_arguments(self, parser):
        parser.add_argument(
            "--since",
            type=lambda s: dateparser.parse(s),
            help="If specified, only the records indexed after than the specified value will be parsed",
        )

        parser.add_argument(
            "--endpoint",
            type=str,
            help="If specified, only the records indexed after than the specified value will be parsed",
        )

    def handle(self, *args, **options):
        # Manage output
        FORMAT = "%(asctime)s %(message)s"
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, format=FORMAT)

        # Actual command
        qs = OpenDataSoftQuery.objects.filter(is_active=True)

        if options["endpoint"]:
            qs = qs.filter(endpoint__name=options["endpoint"])

        if options["since"]:
            since = options["since"].strftime("%Y-%m-%d")
        else:
            since = ""

        if len(qs):
            logging.info(f"{len(qs)} active queries found. Processing...")
            for query in qs:
                query.run(since=since)
        else:
            logging.warning("There is no active query in the database.")
