#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from dateutil import parser as dateparser
from bnsp.models import Query


class Command(BaseCommand):
    help = "Import publications from the BNSP Queries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--since",
            type=lambda s: dateparser.parse(s),
            help="If specified, only the records indexed after than the specified value will be parsed",
        )

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        qs = Query.objects.filter(live=True)

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
