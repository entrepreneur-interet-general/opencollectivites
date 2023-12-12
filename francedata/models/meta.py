from francedata.services.django_admin import TimeStampModel
from django.db import models

# Meta models
class Metadata(TimeStampModel):
    """
    The metadata, as property (prop)/value couples
    """

    prop = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prop}: {self.value}"

    class Meta:
        verbose_name = "métadonnée"


class DataYear(TimeStampModel):
    """
    The years for which we have data stored
    """

    year = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name = "millésime"
        get_latest_by = "year"
