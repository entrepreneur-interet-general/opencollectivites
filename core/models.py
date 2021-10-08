from django.db import models
from django.db.models.query import QuerySet

from francedata.services.django_admin import TimeStampModel
from francedata.models import Commune, Departement, Epci, Region

from urllib.parse import urlparse
from datetime import date, datetime
from taggit.managers import TaggableManager


# Models
class Metadata(TimeStampModel):
    """
    The metadata, as property (prop)/value couples
    """

    prop = models.CharField("propriété", max_length=100, unique=True)
    value = models.CharField("valeur", max_length=255)

    def __str__(self):
        return f"{self.prop}: {self.value}"

    class Meta:
        verbose_name = "métadonnée"


class DataYear(TimeStampModel):
    """
    The years for which we have data stored
    """

    year = models.PositiveSmallIntegerField("année")

    def __str__(self):
        return f"{self.year}"

    class Meta:
        ordering = ["year"]
        verbose_name = "millésime"


class DocumentType(TimeStampModel):
    """
    The types of document
    """

    name = models.CharField("nom", max_length=100)
    icon_path = models.CharField(
        "Chemin de l’icône", max_length=255, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "type de document"
        verbose_name_plural = "types de document"


class PageType(TimeStampModel):
    """
    The types of pages
    """

    name = models.CharField("nom", max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "type de page"
        verbose_name_plural = "types de page"


class Topic(TimeStampModel):
    """
    (fr: Thématique)
    The main topic of a site or document. Used for filtering.
    """

    name = models.CharField("nom", max_length=100)
    icon_path = models.CharField("Chemin de l’icône", max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "thématique"


class Scope(TimeStampModel):
    """
    (fr: Portée)
    The reach of a site or document (national, regional, etc.)
    """

    name = models.CharField("nom", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "portée"


class Organization(TimeStampModel):
    """
    (fr: Organisation)
    An organization (eg, the editor of a site or document)
    """

    name = models.CharField("nom", max_length=100)
    acronym = models.CharField("sigle", max_length=100, blank=True)
    part_of = models.ForeignKey(
        "Organization", blank=True, on_delete=models.SET_NULL, null=True
    )
    logo = models.ImageField(upload_to="logos", blank=True)

    def __str__(self):
        if self.acronym:
            return f"{self.acronym} ({self.name})"
        else:
            return self.name

    def short_name(self):
        if self.acronym:
            return self.acronym
        else:
            return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "organisation"


class Source(TimeStampModel):
    """
    The website where the information is from
    """

    title = models.CharField("titre", max_length=100)
    editor = models.ManyToManyField("Organization", verbose_name="éditeur")
    rss_feed = models.OneToOneField(
        "feeds.Source",
        verbose_name="flux RSS",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
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
    last_update = models.DateField("dernière mise à jour", default=date.today)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.rss_feed and not self.url:
            self.url = self.rss_feed.feed_url

        if not self.title:
            self.title = self.url

        if self.url:
            self.base_domain = urlparse(self.url).hostname[:100]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]


class Document(TimeStampModel):
    """
    A single document or publication.
    """

    url = models.URLField("URL", max_length=512, unique=True)
    title = models.CharField("titre", max_length=255, null=True, blank=True)
    body = models.TextField("corps", blank=True)
    base_domain = models.CharField("domaine", max_length=100, null=True, blank=True)
    is_published = models.BooleanField("est publié", null=True, blank=True)
    publication_pages = models.ManyToManyField(
        PageType, verbose_name="pages de publication", blank=True
    )
    image_url = models.URLField("URL de l’image", max_length=255, blank=True, null=True)
    tags = TaggableManager(related_name="documents_tags", blank=True)
    weight = models.PositiveSmallIntegerField("poids", default=100)
    scope = models.ManyToManyField(Scope, verbose_name="portée", blank=True)
    topics = models.ManyToManyField(Topic, verbose_name="sujet", blank=True)
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
    rss_post = models.ForeignKey(
        "feeds.Post",
        verbose_name="Post associé",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    bnsp_query = models.ForeignKey(
        "bnsp.Query",
        verbose_name="Requête Gallica associée",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ods_queries = models.ManyToManyField(
        "external_apis.OpenDataSoftQuery",
        verbose_name="Requête OpenDataSoft associée",
        blank=True,
    )
    document_type = models.ManyToManyField(
        DocumentType, verbose_name="type de document", blank=True
    )
    last_update = models.DateField("dernière mise à jour", null=True, blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.url

    def save(self, *args, **kwargs):
        self.base_domain = urlparse(self.url).hostname[:100]
        if not self.last_update:
            self.last_update = datetime.now()

        super().save(*args, **kwargs)

    def get_props_from_source(self, props: list = None) -> None:
        """
        Copies a list of properties from the source
        """
        if not props:
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
            for value in getattr(self.source, prop).all():
                getattr(self, prop).add(value)

    def identify_regions(self, text: str) -> None:
        """
        Tries to identify the name of a région in the given string
        """
        regions = Region.objects.all()
        for region in regions:
            if region.name in text:
                self.regions.add(region)
        self.save()

    def identify_departements(self, text: str) -> None:
        """
        Tries to identify the name of a département in the given string
        """
        departements = Departement.objects.all()
        for departement in departements:
            if departement.name in text:
                self.departements.add(departement)
        self.save()

    def identify_metropoles(self, text: str) -> None:
        """
        Tries to identify the name of a métropole in the given string
        """
        metropoles = Epci.objects.filter(epci_type__in=["MET69", "METRO"])
        for metropole in metropoles:
            if metropole.name in text:
                self.epcis.add(metropole)
        self.save()

    def identify_main_cities_by_departement(
        self, text: str, departements: QuerySet
    ) -> None:
        """
        Tries to identify the name of the city in the given string.
        The city has to belong to the main cities in France and be in the given list of departements.
        """
        main_cities = Commune.get_main_cities()

        for departement in departements:
            main_cities_in_departement = main_cities.filter(departement=departement)
            for city in main_cities_in_departement:
                if city.name in text:
                    self.communes.add(city)
        self.save()

    def identify_main_cities_by_region(self, text: str, regions: QuerySet) -> None:
        """
        Tries to identify the name of the city in the given string.
        The city has to belong to the main cities in France and be in the given list of regions.
        """
        main_cities = Commune.get_main_cities()

        for region in regions:
            main_cities_in_region = main_cities.filter(departement__region=region)
            for city in main_cities_in_region:
                if city.name in text:
                    self.communes.add(city)
        self.save()
