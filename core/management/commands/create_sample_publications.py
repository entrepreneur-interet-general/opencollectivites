#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from core.models import Document, DocumentType, Metadata, Source, PageType, Scope, Topic

from random import choice, choices, randrange
from pprint import pprint

from datetime import datetime

"""
Ce script crée des publications d'exemple.
⚠️ Ne pas utiliser sur le serveur de production
"""

DEFAULT_QUANTITY = 10


class Command(BaseCommand):
    help = "Creates 'quantity' sample publications."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quantity",
            type=int,
            help=f"If specified, the given number of posts will be created (default: {DEFAULT_QUANTITY})",
        )

    def handle(self, *args, **options):
        """
        Main command
        """
        # Get the number of publications to create
        if options["quantity"]:
            quantity = options["quantity"]
        else:
            quantity = DEFAULT_QUANTITY

        # If the script has been run in the past, there is an entry in the Metadata.
        # Get the last sample number, to increment from there
        last_sample_entry, return_code = Metadata.objects.get_or_create(
            prop="sample_posts_last_id"
        )
        if return_code:
            # If the prop was not in metadata, the database is empty
            last_sample = 0
            last_sample_entry.value = 0
            last_sample_entry.save()
        else:
            last_sample = int(last_sample_entry.value)

        new_entry_number = last_sample + 1
        last_entry_number = last_sample + quantity
        print(
            f"📝  Creating {quantity} new publications, starting at number {new_entry_number}"
        )

        while new_entry_number < last_entry_number:
            create_sample_publication(new_entry_number)
            new_entry_number += 1

        last_sample_entry.value = new_entry_number
        last_sample_entry.save()


def create_sample_publication(entry_number):
    """
    Creates a sample publication.
    """
    url = f"https://example.open-collectivites.fr/{entry_number}"
    new_doc, return_code_doc = Document.objects.get_or_create(url=url)

    new_doc.title = f"Publication de test #{entry_number}"
    new_doc.base_domain = "example.open-collectivites.fr"
    new_doc.is_published = True
    new_doc.last_update = datetime.now()

    body_list = []
    # Randomize characteristics
    new_doc.source = choice(Source.objects.all())
    body_list.append(f"Source: {new_doc.source}")

    publication_pages = random_many_to_many(PageType)
    new_doc.publication_pages.set(publication_pages)
    body_list.append(
        f"Publication pages: {', '.join([str(i) for i in publication_pages])}"
    )

    scopes = random_many_to_many(Scope)
    new_doc.scope.set(scopes)
    body_list.append(f"Scope: {', '.join([str(i) for i in scopes])}")

    topics = random_many_to_many(Topic)
    new_doc.topics.set(topics)
    body_list.append(f"Topics: {', '.join([str(i) for i in topics])}")

    new_doc.document_type.set([DocumentType.objects.get(id=1)])

    pprint(body_list)
    new_doc.body = " — ".join(body_list)

    new_doc.save()


def random_many_to_many(model):
    """
    Returns a random number of values from a model for many-to-many fields
    """
    all_entries = model.objects.all()
    return choices(all_entries, k=randrange(1, all_entries.count()))
