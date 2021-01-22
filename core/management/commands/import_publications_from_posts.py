#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from feeds.models import Post
from core.models import Metadata, Source, Document, Scope

from urllib.parse import urlparse
from dateutil import parser as dateparser
from pprint import pprint

"""
Ce script importe les publications depuis les posts gérés dans les flux RSS
"""


class Command(BaseCommand):
    help = "Import posts from the Feeds to the Core one."

    def add_arguments(self, parser):
        parser.add_argument(
            "--since",
            type=lambda s: dateparser.parse(s),
            help="If specified, only the posts more recent than the specified value will be parsed",
        )

    def handle(self, *args, **options):
        if options["since"]:
            last_update = options["since"]
        else:
            try:
                last_update_value = Metadata.objects.get(prop="ipfp_last_update")
                last_update = dateparser.parse(last_update_value)
            except ObjectDoesNotExist as e:
                last_update = None

        if last_update:
            posts = Post.objects.filter(created__gte=sd)
        else:
            posts = Post.objects.all()

        for post in posts:
            new_doc, return_code_doc = Document.objects.get_or_create(url=post.link)
            if return_code_doc:
                print(f"📜  New publication created from RSS post {post.title}")
                new_doc.title = post.title[:255]
                new_doc.rss_post = post

                source_entry, return_code_source = Source.objects.get_or_create(
                    rss_feed=post.source
                )
                if return_code_source:
                    source_entry.title = post.source.name
                    source_entry.url = post.source.site_url
                    source_entry.base_domain = urlparse(source_entry.url).hostname

                else:
                    # Copy many-to-many entries that automatically apply to all documents from this source
                    props = [
                        "regions",
                        "departements",
                        "epcis",
                        "communes",
                        "scope",
                        "topics",
                        "document_type",
                    ]
                    for prop in props:
                        getattr(new_doc, prop).set(getattr(source_entry, prop).all())

                source_entry.last_update = post.source.last_change
                source_entry.save()
                new_doc.source = source_entry
                new_doc.last_update = post.created

                new_doc.save()
            else:
                print(f"📜  Publication {new_doc.title} already in database")
