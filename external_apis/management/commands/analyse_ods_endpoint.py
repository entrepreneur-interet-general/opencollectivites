#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand
from dateutil import parser as dateparser
from external_apis.services.analyse_ods import analyse_endpoint


class Command(BaseCommand):
    help = "Analyse datasets for an OpenDataSoft endpoint."

    def add_arguments(self, parser):
        parser.add_argument(
            "endpoint",
            type=str,
            help="Root URL of the endpoint to analyse",
        )

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        endpoint = options["endpoint"]
        analyse_endpoint(endpoint)
