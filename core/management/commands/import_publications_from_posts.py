#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils.html import strip_tags

from feeds.models import Post
from core.models import Metadata, Source, Document

from urllib.parse import urlparse
from dateutil import parser as dateparser
from datetime import datetime
from pytz import UTC

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
        last_update_entry, return_code_lu = Metadata.objects.get_or_create(
            prop="ipfp_last_update"
        )
        if options["since"]:
            last_update = options["since"]
        elif return_code_lu:
            # If the prop was not in metadata, the database is empty
            last_update = None
        else:
            last_update = dateparser.parse(last_update_entry.value)

        if last_update:
            last_update = UTC.localize(last_update)
            print(f"🗓️  Importing new posts since last update ({last_update})")
            posts = Post.objects.filter(created__gte=last_update)
        else:
            print(f"⏳  Importing all posts since the beginning")
            posts = Post.objects.all()

        for post in posts:
            new_doc, return_code_doc = Document.objects.get_or_create(url=post.link)
            if return_code_doc:
                print(f"📜  New publication created from RSS post {post.title}")

                # Only do source-related part on first creation
                source_entry, return_code_source = Source.objects.get_or_create(
                    rss_feed=post.source
                )
                if return_code_source:
                    source_entry.title = post.source.name
                    source_entry.url = post.source.site_url
                    source_entry.base_domain = urlparse(source_entry.url).hostname[:100]

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

            else:
                print(f"📜  Publication {new_doc.title} already in database, updating.")
            new_doc.title = strip_tags(post.title[:255])
            new_doc.rss_post = post

            new_doc.body = strip_tags(post.body)
            new_doc.image_url = post.image_url

            new_doc.last_update = post.created

            new_doc.save()

        current_time = datetime.now().isoformat()
        last_update_entry.value = current_time
        last_update_entry.save()
