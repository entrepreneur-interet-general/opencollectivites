from django.db import models
from francedata.models.collectivity import Commune, Departement, Epci, Region
from francedata.services.django_admin import TimeStampModel
from francedata.services.validators import validate_siren

COLLECTIVITY_TYPES = [
    ("COMM", "Communes"),
    ("DEPT", "Départements"),
    ("EPCI", "EPCIs"),
    ("REG", "Régions"),
]


class Vintage(TimeStampModel):
    """
    The vintages parameters, same as in Aspic
    """

    key = models.CharField("clef", max_length=100)
    value = models.CharField("valeur", max_length=100)

    def __str__(self):
        return f"{self.key}"

    class Meta:
        verbose_name = "millésime"


class DataTable(TimeStampModel):
    """
    A data table for a given page
    """

    name = models.CharField("nom", max_length=100)
    page_type = models.CharField(
        "type de fiche", max_length=4, choices=COLLECTIVITY_TYPES
    )
    slug = models.SlugField("slug", max_length=120, unique=True)

    def __str__(self):
        return f"{self.page_type}: {self.name}"

    class Meta:
        verbose_name = "tableau"
        verbose_name_plural = "tableaux"


class DataRow(TimeStampModel):
    """
    A row for a given data table
    """

    table = models.ForeignKey("DataTable", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField("rang", default=0)
    key = models.CharField("code", max_length=50)
    label = models.CharField("libellé", max_length=250)
    tooltip = models.CharField("infobulle", max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.table}: {self.label} ({self.key})"

    class Meta:
        verbose_name = "ligne de tableau"
        verbose_name_plural = "lignes de tableau"
        ordering = ["table", "rank"]


class CollectivityMessage(TimeStampModel):
    """
    A message related to a specific community
    """

    collectivity_type = models.CharField(
        "type de collectivité", max_length=4, choices=COLLECTIVITY_TYPES
    )

    collectivity_slug = models.CharField("slug collectivité", max_length=50)
    message = models.TextField("message")

    class Meta:
        verbose_name = "message lié à une collectivité"
        verbose_name_plural = "messages liés à une collectivité"

    def __str__(self):
        return f"{self.collectivity_type} : {self.get_coll_name()}"

    def get_coll_name(self) -> str:
        """
        Returns the name of the collectivity
        """
        if self.collectivity_type == "COMM":
            model = Commune
        elif self.collectivity_type == "DEPT":
            model = Departement
        elif self.collectivity_type == "REG":
            model = Region
        elif self.collectivity_type == "EPCI":
            model = Epci
        else:
            raise ValueError("Unknown collectivity type")

        collectivity = model.objects.filter(slug=self.collectivity_slug).first()

        if collectivity:
            return str(collectivity)
        else:
            return "Collectivity not found"
