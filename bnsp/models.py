from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from core.models import Document, Source
from francedata.services.django_admin import TimeStampModel
from bnsp.services.gallica_search_api import GallicaSearch, Record


class Query(TimeStampModel):
    # A query on the Gallica Search API
    name = models.CharField(max_length=255, verbose_name="nom")
    query = models.CharField(max_length=255, verbose_name="requête")

    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, verbose_name="source associée"
    )

    last_polled = models.DateTimeField(
        blank=True, null=True, verbose_name="dernière tentative"
    )
    last_success = models.DateTimeField(
        blank=True, null=True, verbose_name="dernière réussite"
    )
    last_change = models.DateTimeField(
        blank=True, null=True, verbose_name="dernier changement"
    )
    live = models.BooleanField(default=True, verbose_name="requête active")

    class Meta:
        verbose_name = "requête"

    def __str__(self):
        return f"{self.name}"

    def run(self) -> dict:
        print(f"running query {self.query}")
        search = GallicaSearch(max_records=50)

        response = search.get_records(self.query)

        if len(response):
            for record in search.records.values():
                self.create_or_update_document(record)

        return response

    def create_or_update_document(self, record: Record):
        new_doc, return_code_doc = Document.objects.get_or_create(url=record.ark_url)
        if return_code_doc:
            print(f"📜  New publication created from Gallica record {record.title}")

        new_doc.source = self.source

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
            getattr(new_doc, prop).set(getattr(self.source, prop).all())

        # The indexation date is alas not in the record data
        now = timezone.now()
        new_doc.last_update = now

        new_doc.title = strip_tags(record.title[:255])

        # The description
        new_doc.body = ", ".join(record.get_values("dc:subject"))
        new_doc.image_url = record.get_thumbnail()

        new_doc.save()
