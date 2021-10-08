import logging
from dateutil import parser as dateparser
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from francedata.services.django_admin import TimeStampModel
from core.models import Document, Source
from external_apis.abstract import ExternalApiQuery
from external_apis.services.opendatasoft_api import OpenDataSoftSearch
from simple_history.models import HistoricalRecords


class DataMapping(TimeStampModel):
    name = models.CharField("nom", max_length=100)
    source_field = models.CharField(
        "champ source", max_length=100, blank=True, null=True
    )
    mapping = models.JSONField("données")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Table de correspondance"
        verbose_name_plural = "tables de correspondance"

    def __str__(self):
        return self.name


class OpenDataSoftEndpoint(TimeStampModel):
    name = models.CharField("nom", max_length=100)
    url = models.URLField("url")
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, verbose_name="source associée"
    )

    class Meta:
        verbose_name = "OpenDataSoft — point d’accès"
        verbose_name_plural = "OpenDataSoft — points d’accès"

    def __str__(self):
        return self.name


class OpenDataSoftQuery(ExternalApiQuery):
    # A query on the OpenDataSoft Search API
    # Retrieves a list of datasets
    endpoint = models.ForeignKey(
        OpenDataSoftEndpoint, on_delete=models.CASCADE, verbose_name="point d’accès"
    )

    mapping = models.ManyToManyField(
        DataMapping, verbose_name="table de correspondance", blank=True
    )

    identify_regions = models.BooleanField(
        verbose_name="Identifier les noms de régions", default=False
    )
    identify_departements = models.BooleanField(
        verbose_name="Identifier les noms de départements", default=False
    )
    identify_metropoles = models.BooleanField(
        verbose_name="Identifier les noms de métropoles", default=False
    )

    class Meta:
        verbose_name = "OpenDataSoft — requête"
        unique_together = ["query", "endpoint"]

    def run(self, since: str = "") -> None:
        logging.info(f"running query {self.name} ({self.query})")

        now = timezone.now()

        self.last_polled = now
        self.save()

        # Add mandatory filters to query
        if since:
            modified_date = since
        elif self.last_success:
            modified_date = self.last_success.strftime("%Y-%m-%d")
        else:
            modified_date = "2016-01-01"

        if self.query in ["all", "tout", "*"]:
            query = f"modified >= date'{modified_date}'"
        else:
            query = f"{self.query} and modified >= date'{modified_date}'"

        ods = OpenDataSoftSearch(self.endpoint.url)

        results = ods.catalog_datasets(where=query, exclude="theme:INTERNE")

        if len(results):
            for result in results:
                self.create_or_update_document(result)
            self.last_change = now

        self.last_success = now
        self.save()

    def create_or_update_document(self, result: dict) -> None:
        """
        Creates or updates a Document object based on a result from an ODS Catalog query
        """
        metadata = result["dataset"]["metas"]["default"]
        title = metadata["title"] or ""
        description = metadata["description"] or ""

        dataset_id = result["dataset"]["dataset_id"]

        url = f"{self.endpoint.url}/explore/dataset/{dataset_id}/"

        new_doc, return_code_doc = Document.objects.get_or_create(url=url)
        if return_code_doc:
            logging.info(
                f"📜  New publication created from {self.endpoint.name} dataset {title}"
            )

            new_doc.last_update = dateparser.parse(metadata["modified"])
        else:
            logging.info(
                f"📜  Publication from {self.endpoint.name} dataset {title} updated"
            )

        new_doc.ods_queries.add(self)
        new_doc.source = self.endpoint.source

        new_doc.is_published = True

        new_doc.get_props_from_source()

        new_doc.title = strip_tags(title[:255])
        new_doc.body = strip_tags(description)

        new_doc.save()

        # Extra filters
        if self.mapping.count():
            self.apply_mappings(new_doc, metadata)

        full_text = " - ".join([title, description])
        if self.identify_regions:
            new_doc.identify_regions(full_text)

        if self.identify_departements:
            new_doc.identify_departements(full_text)

        if self.identify_metropoles:
            new_doc.identify_metropoles(full_text)

    def apply_mappings(self, document: Document, metadata: dict) -> None:
        """
        Applies the selected mappings to the document
        """
        for mapping in self.mapping.all():
            self.add_metadata_with_mapping(document, metadata, mapping)

    def add_metadata_with_mapping(
        self, document: Document, metadata: dict, mapping: DataMapping
    ) -> None:
        """
        Adds metadata to the document according to a mapping item
        """
        field = mapping.source_field
        mapping_values = mapping.mapping

        if field in metadata:
            metadata_values = metadata[field]
            for mapping_value, properties in mapping_values.items():
                if mapping_value in metadata_values:
                    if isinstance(properties, list):
                        for property in properties:
                            self.add_metadata_properties(document, property)
                    else:
                        self.add_metadata_properties(document, properties)

    def add_metadata_properties(self, document: Document, properties: dict) -> None:
        """
        Add metadata from a properties dict
        """
        if properties["type"] == "topic":
            document.topics.add(properties["value"])
        elif properties["type"] == "scope":
            document.scope.add(properties["value"])
        elif properties["type"] == "publication_pages":
            document.publication_pages.add(properties["value"])
        elif properties["type"] == "region":
            document.regions.add(properties["value"])
        elif properties["type"] == "region":
            document.regions.add(properties["value"])

        document.save()
