from ninja import Schema
from typing import List


class TopicSchema(Schema):
    id: int
    name: str
    icon_url: str = None


class PageTypeSchema(Schema):
    id: int
    name: str


class ScopeSchema(Schema):
    id: int
    name: str


class DocumentSchema(Schema):
    url: str
    title: str
    base_domain: str
    publication_pages: List[PageTypeSchema]
    scope: List[ScopeSchema]

    """
    scope = models.ManyToManyField(Scope, verbose_name="portée", blank=True)
    topics = models.ManyToManyField(Topic, verbose_name="sujet", blank=True)
    years = models.ManyToManyField(DataYear, blank=True)
    regions = models.ManyToManyField(
        "francesubdivisions.Region", verbose_name="région", blank=True
    )
    departements = models.ManyToManyField(
        "francesubdivisions.Departement",
        verbose_name="département",
        blank=True,
    )
    epcis = models.ManyToManyField(
        "francesubdivisions.Epci",
        verbose_name="EPCI",
        blank=True,
    )
    communes = models.ManyToManyField(
        "francesubdivisions.Commune",
        verbose_name="commune",
        blank=True,
    )
    source = models.ForeignKey(
        "Source", on_delete=models.SET_NULL, null=True, blank=True
    )
    rss_post = models.ForeignKey(
        "feeds.Post",
        verbose_name="Post associé",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    document_type = models.ManyToManyField(
        DocumentType, verbose_name="type de document", blank=True
    )
    last_update = models.DateField("dernière mise à jour", null=True, blank=True)
    """