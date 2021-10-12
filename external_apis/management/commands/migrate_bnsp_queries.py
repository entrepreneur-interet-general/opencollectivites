#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from bnsp.models import Query
from core.models import Document
from external_apis.models import BnspQuery
from pprint import pprint


class Command(BaseCommand):
    help = "Analyse datasets for an OpenDataSoft endpoint."

    def handle(self, *args, **options):
        queries = Query.objects.all()

        for q in queries:
            new_item, _ = BnspQuery.objects.update_or_create(
                id=q.id,
                name=q.name,
                query=q.query,
                source=q.source,
                is_active=q.is_active,
                identify_departements=q.identify_departements,
                identify_main_cities=q.identify_main_cities,
                identify_metropoles=q.identify_metropoles,
                identify_regions=q.identify_regions,
            )
            new_item.save()

        docs = Document.objects.filter(bnsp_query__isnull=False)
        for doc in docs:
            qid = doc.bnsp_query_id
            doc.bnsp_queries.add(qid)
            doc.save()
