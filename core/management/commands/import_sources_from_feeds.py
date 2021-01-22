#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from feeds.models import Source as FeedsSource
from core.models import Source as CoreSource

from urllib.parse import urlparse
from dateutil import parser as dateparser
from pprint import pprint

"""
Ce script importe les sources depuis celles présentes dans les flux RSS
"""


class Command(BaseCommand):
    help = "Import sources from the Feeds module to the Core one."

    def handle(self, *args, **options):
        feed_sources = FeedsSource.objects.all()

        for feed_source in feed_sources:
            core_source_entry, return_code = CoreSource.objects.get_or_create(
                rss_feed=feed_source
            )
            if return_code:
                core_source_entry.title = feed_source.name
                core_source_entry.url = feed_source.site_url
                print(f"ℹ️  new source {core_source_entry.title} created")
            else:
                print(f"ℹ️  existing source {core_source_entry.title} updated")

            core_source_entry.last_update = feed_source.last_change
            core_source_entry.save()
