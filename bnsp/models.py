from dateutil import parser as dateparser
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from core.models import DataYear, Document, Source
from francedata.services.django_admin import TimeStampModel
from bnsp.services.gallica_search_api import GallicaSearch, Record
import logging


class Query(TimeStampModel):
    # A query on the Gallica Search API
    name = models.CharField(max_length=255, verbose_name="nom", unique=True)
    query = models.CharField(max_length=1000, verbose_name="requête", unique=True)

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

    def __str__(self) -> str:
        return f"{self.name}"

    def run(self, since: str = "") -> None:
        logging.info(f"running query {self.query}")

        now = timezone.now()

        self.last_polled = now
        self.save()

        if since:
            indexation_date = since
        elif self.last_success:
            indexation_date = self.last_success.strftime("%Y%m%d")
        else:
            indexation_date = "20160101"

        # search = GallicaSearch(max_records=50, endpoint="https://www.bnsp.insee.fr/SRU")
        # Temporary fix to get BNSP urls while they fix their endpoint (cf #OC-213)
        search = GallicaSearch(max_records=50)
        dated_query = f'({self.query}) and dc.date >= "2016" and indexationdate >= "{indexation_date}"'
        search.fetch_records(dated_query)

        records = search.get_records().values()
        if len(records):
            for record in records:
                self.create_or_update_document(record)
            self.last_change = now

        self.last_success = now
        self.save()

    def create_or_update_document(self, record: Record) -> None:
        """
        Creates or updates a Document object based on a Record retrieved from
        Gallica or a white-label of it.
        """

        # Temporary fix to get BNSP urls while they fix their endpoint (cf #OC-213)
        record.ark_url = record.ark_url.replace("gallica.bnf.fr", "www.bnsp.insee.fr")

        new_doc, return_code_doc = Document.objects.get_or_create(url=record.ark_url)
        if return_code_doc:
            logging.info(
                f"📜  New publication created from Gallica record {record.title}"
            )

            # The indexation date is alas not in the record data
            now = timezone.now()
            new_doc.last_update = now
        else:
            logging.info(f"📜  Publication from Gallica record {record.title} updated")

        new_doc.bnsp_query = self
        new_doc.source = self.source

        new_doc.is_published = True

        new_doc.get_props_from_source()

        new_doc.title = strip_tags(record.title[:255])

        # Document vintage
        try:
            date = dateparser.parse(record.date).strftime("%Y")
            year, _ = DataYear.objects.get_or_create(year=date)
            new_doc.years.add(year)
        except dateparser._parser.ParserError:
            pass

        # tags
        for tag in record.get_values("dc:subject"):
            cap_tag = tag[:1].upper() + tag[1:]
            new_doc.tags.add(cap_tag)

        # The description
        new_doc.body = ", ".join(record.get_values("dc:subject"))
        new_doc.image_url = record.get_thumbnail()

        new_doc.save()
