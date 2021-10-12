#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from dateutil import parser as dateparser
from external_apis.models import BnspQuery


class Command(BaseCommand):
    help = "Import publications from the BNSP Queries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--since",
            type=lambda s: dateparser.parse(s),
            help="If specified, only the records indexed after than the specified value will be parsed",
        )

        parser.add_argument(
            "--query",
            type=int,
            help="If specified, only query with the specified id will run",
        )

    def handle(self, *args, **options):
        # Manage output
        FORMAT = "%(asctime)s %(message)s"
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, format=FORMAT)

        if options["query"]:
            qs = BnspQuery.objects.filter(id=options["query"])
        else:
            qs = BnspQuery.objects.filter(is_active=True)

        if options["since"]:
            since = options["since"].strftime("%Y%m%d")
        else:
            since = ""

        if len(qs):
            logging.info(f"{len(qs)} active queries found. Processing...")
            for query in qs:
                query.run(since=since)
        else:
            logging.warning("There is no active query in the database.")
