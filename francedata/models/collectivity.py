from francedata.services.django_admin import TimeStampModel
from django.db import models

from francedata.models.meta import DataYear

from unidecode import unidecode
from django.db import models
from django.db.models import Max
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.text import slugify

from francedata.services.django_admin import TimeStampModel
from francedata.services.validators import (
    validate_insee_region,
    validate_insee_departement,
    validate_insee_commune,
    validate_siren,
)


# France administrative structure models


class CollectivityModel(TimeStampModel):
    """
    Abstract model for common methods used by the following ones
    """

    class Meta:
        abstract = True

    def get_data(self, year: int = None, datacode: str = None):
        """
        Get the data for the given year (by default, the most recent one)
        If a datacode is provided, return only this data point
        """
        if not year:
            year = self.years.aggregate(Max("year"))["year__max"]
        data = self.regiondata_set.filter(year__year=year)

        if datacode:
            data = data.filter(datacode=datacode)

        return data

    def add_current_datayear(self):
        """
        Adds the current datayear to a collectivity object
        """
        year = str(timezone.now().year)
        year_entry, _ = DataYear.objects.get_or_create(year=year)
        self.years.add(year_entry)
        self.save()

    def create_slug(self):
        self.slug = slugify(unidecode(self.name))

    def save(self, *args, **kwargs):
        self.full_clean()
        self.create_slug()
        return super().save(*args, **kwargs)


class Region(CollectivityModel):
    """
    A French région
    """

    class RegionCategory(models.TextChoices):
        REG = "REG", "Région"
        CTU = "CTU", "Collectivité territoriale unique"

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    insee = models.CharField(
        "identifiant Insee", max_length=2, validators=[validate_insee_region]
    )
    siren = models.CharField(
        "numéro Siren", max_length=9, validators=[validate_siren], blank=True, null=True
    )
    category = models.CharField(
        max_length=3,
        choices=RegionCategory.choices,
        null=True,
        blank=True,
        verbose_name="catégorie",
    )
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "région"
        unique_together = (("name", "insee"),)

    def __str__(self):
        return self.name

    def subdivisions_count(self):
        return {
            "departements": self.departement_set.all().count(),
            "communes": Commune.objects.filter(departement__region=self).count(),
        }


class Departement(CollectivityModel):
    """
    A French département
    """

    class DepartementCategory(models.TextChoices):
        DEPT = "DEPT", "Département"
        PARIS = "PARIS", "Paris"
        ML = "ML", "Métropole de Lyon"

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    region = models.ForeignKey(
        "Region", on_delete=models.CASCADE, verbose_name="région", blank=True, null=True
    )
    insee = models.CharField(
        "identifiant Insee", max_length=3, validators=[validate_insee_departement]
    )
    siren = models.CharField(
        "numéro Siren", max_length=9, validators=[validate_siren], blank=True, null=True
    )
    category = models.CharField(
        max_length=5,
        choices=DepartementCategory.choices,
        null=True,
        blank=True,
        verbose_name="catégorie",
    )
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "département"

    def __str__(self):
        return f"{self.insee} - {self.name}"

    def list_epcis(self) -> QuerySet:
        epci_ids = list(
            self.commune_set.all().values_list("epci__id", flat=True).distinct()
        )
        if None in epci_ids:
            # It happens for departements that have isolated communes
            epci_ids.remove(None)

        return Epci.objects.filter(id__in=epci_ids)


class Epci(CollectivityModel):
    """
    A French établissement public de coopération intercommunale
    à fiscalité propre
    """

    class EpciType(models.TextChoices):
        CA = "CA", "Communauté d’agglomération"
        CC = "CC", "Communauté de communes"
        CU = "CU", "Communauté urbaine"
        MET69 = "MET69", "Métropole de Lyon"
        METRO = "METRO", "Métropole"

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    epci_type = models.CharField(
        max_length=5,
        null=True,
        choices=EpciType.choices,
        verbose_name="type d’EPCI",
        blank=True,
    )
    siren = models.CharField("numéro Siren", max_length=9, validators=[validate_siren])
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "EPCI"

    def __str__(self):
        return self.name

    def create_slug(self):
        self.slug = slugify(f"{unidecode(self.name)}-{self.siren}")


class Commune(CollectivityModel):
    """
    A French commune
    """

    name = models.CharField("nom", max_length=100)
    years = models.ManyToManyField(DataYear, verbose_name="millésimes")
    departement = models.ForeignKey(
        "Departement", on_delete=models.CASCADE, verbose_name="département"
    )
    epci = models.ForeignKey(
        "Epci", on_delete=models.CASCADE, null=True, verbose_name="EPCI", blank=True
    )
    insee = models.CharField(
        "identifiant Insee", max_length=5, validators=[validate_insee_commune]
    )
    siren = models.CharField(
        "numéro Siren", max_length=9, validators=[validate_siren], blank=True
    )
    population = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "commune"

    def __str__(self):
        return f"{self.name} ({self.departement})"

    def create_slug(self):
        self.slug = slugify(f"{unidecode(self.name)}-{self.insee}")

    @classmethod
    def get_prefectures(cls) -> QuerySet:
        """
        Returns a queryset with all préfectures
        """
        return cls.objects.filter(
            insee__in=DepartementData.objects.filter(datacode="seat_insee").values_list(
                "value", flat=True
            )
        )

    @classmethod
    def get_main_cities_by_population(cls, population: int = 50000) -> QuerySet:
        """
        Returns a queryset with cities over a set population (default: 50 000)
        """
        return cls.objects.filter(population__gt=population)

    @classmethod
    def get_main_cities(cls) -> QuerySet:
        """
        Returns a queryset that combines préfectures and most populated cities
        """
        prefectures = cls.get_prefectures()
        most_populated = cls.get_main_cities_by_population()
        return prefectures | most_populated


# France collectivities data models
class CollectivityDataModel(TimeStampModel):
    """
    Abstract model for common methods used by the following ones
    """

    # (Missing here: "collectivity" variable, specific to the relevant collectivity level)
    year = models.ForeignKey(
        "DataYear", on_delete=models.PROTECT, verbose_name="millésime"
    )
    datacode = models.CharField("code", max_length=255)
    value = models.CharField("valeur", max_length=255, blank=True, null=True)
    label = models.CharField("label", max_length=255, blank=True, null=True)
    datatype = models.CharField("type", max_length=255, blank=True, null=True)
    source = models.ForeignKey(
        "DataSource", on_delete=models.PROTECT, verbose_name="source"
    )

    class Meta:
        abstract = True


class RegionData(CollectivityDataModel):
    region = models.ForeignKey(
        "Region", on_delete=models.CASCADE, verbose_name="région"
    )

    class Meta:
        verbose_name = "donnée région"
        verbose_name_plural = "données région"
        constraints = [
            models.UniqueConstraint(
                fields=["region", "year", "datacode"], name="fd_unique_region_data"
            )
        ]

    def __str__(self):
        return f"{self.region.name} - {self.year.year} - {self.datacode}: {self.value}"


class DepartementData(CollectivityDataModel):
    departement = models.ForeignKey(
        "Departement", on_delete=models.CASCADE, verbose_name="département"
    )

    class Meta:
        verbose_name = "donnée département"
        verbose_name_plural = "données département"
        constraints = [
            models.UniqueConstraint(
                fields=["departement", "year", "datacode"],
                name="fd_unique_departement_data",
            )
        ]

    def __str__(self):
        return f"{self.departement.name} - {self.year.year} - {self.datacode}: {self.value}"


class EpciData(CollectivityDataModel):
    epci = models.ForeignKey("Epci", on_delete=models.CASCADE, verbose_name="EPCI")

    class Meta:
        verbose_name = "donnée EPCI"
        verbose_name_plural = "données EPCI"
        constraints = [
            models.UniqueConstraint(
                fields=["epci", "year", "datacode"],
                name="fd_unique_epci_data",
            )
        ]

    def __str__(self):
        return f"{self.epci.name} - {self.year.year} - {self.datacode}: {self.value}"


class CommuneData(CollectivityDataModel):
    commune = models.ForeignKey(
        "Commune", on_delete=models.CASCADE, verbose_name="commune"
    )

    class Meta:
        verbose_name = "donnée commune"
        verbose_name_plural = "données commune"
        constraints = [
            models.UniqueConstraint(
                fields=["commune", "year", "datacode"],
                name="fd_unique_commune_data",
            )
        ]

    def __str__(self):
        return f"{self.commune.name} - {self.year.year} - {self.datacode}: {self.value}"
