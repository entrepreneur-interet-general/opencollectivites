from ninja import Schema
from typing import List
from datetime import date


class TopicSchema(Schema):
    id: int
    name: str
    icon_path: str = None


class DocumentTypeSchema(Schema):
    id: int
    name: str
    icon_path: str = None


class PageTypeSchema(Schema):
    id: int
    name: str


class ScopeSchema(Schema):
    id: int
    name: str


class FilterSchema(Schema):
    scopes: List[ScopeSchema]
    topics: List[TopicSchema]
    document_types: List[DocumentTypeSchema]


class OrganizationSchema(Schema):
    id: int
    name: str
    acronym: str
    part_of: "OrganizationSchema" = None
    logo: str = None


OrganizationSchema.update_forward_refs()


class SourceSchema(Schema):
    id: int
    title: str
    last_update: date
    editor: List[OrganizationSchema]
    """
    url = models.URLField("URL", null=True, blank=True)
    base_domain = models.CharField("domaine", max_length=100, null=True, blank=True)
    scope = models.ManyToManyField(Scope, verbose_name="portée", blank=True)
    topics = models.ManyToManyField(Topic, verbose_name="sujet", blank=True)
    years = models.ManyToManyField(DataYear, verbose_name="année", blank=True)
    regions = models.ManyToManyField(
        "francedata.Region", verbose_name="région", blank=True
    )
    departements = models.ManyToManyField(
        "francedata.Departement",
        verbose_name="département",
        blank=True,
    )
    epcis = models.ManyToManyField(
        "francedata.Epci",
        verbose_name="EPCI",
        blank=True,
    )
    communes = models.ManyToManyField(
        "francedata.Commune",
        verbose_name="commune",
        blank=True,
    )
    document_type = models.ManyToManyField(
        DocumentType,
        verbose_name="type des documents inclus",
        blank=True,
        related_name="documents_type",
    )
    source_type = models.ManyToManyField(
        DocumentType,
        verbose_name="type de source",
        blank=True,
        related_name="source_type",
    )
    """


class DocumentSchema(Schema):
    id: int
    url: str
    title: str
    """
    base_domain: str
    image_url: str = None
    publication_pages: List[PageTypeSchema]
    scope: List[ScopeSchema]
    topics: List[TopicSchema] = None
    document_type: List[DocumentTypeSchema] = None
    last_update: date
    source: SourceSchema
    body: str = None
    """

    """
    years = models.ManyToManyField(DataYear, blank=True)
    regions = models.ManyToManyField(
        "francedata.Region", verbose_name="région", blank=True
    )
    departements = models.ManyToManyField(
        "francedata.Departement",
        verbose_name="département",
        blank=True,
    )
    epcis = models.ManyToManyField(
        "francedata.Epci",
        verbose_name="EPCI",
        blank=True,
    )
    communes = models.ManyToManyField(
        "francedata.Commune",
        verbose_name="commune",
        blank=True,
    )
    source = models.ForeignKey(
        "Source", on_delete=models.SET_NULL, null=True, blank=True
    )
    """
