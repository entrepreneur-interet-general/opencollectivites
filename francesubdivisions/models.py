from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from stdnum.fr import siren
from django.utils.translation import gettext_lazy as _

# Validators
validate_insee_commune = RegexValidator(r"^\d[0-9AB][0-9P]\d\d$")


def validate_siren(value):
    try:
        siren.validate(value)
    except (InvalidChecksum, InvalidFormat, InvalidLength):
        raise ValidationError(
            _("%(value)s is not an valid siren id"),
            params={"value": value},
        )


# Models
class Region(models.Model):
    """
    A French région
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    insee = models.CharField(max_length=2)
    siren = models.CharField(max_length=9)

    def __str__(self):
        return self.name


class Departement(models.Model):
    """
    A French département
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    region = models.ForeignKey("Region", on_delete=models.CASCADE)
    insee = models.CharField(max_length=3)
    siren = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.insee} - {self.name}"


class Epci(models.Model):
    """
    A French établissement public de coopération intercommunale
    à fiscalité propre
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    insee = models.CharField(max_length=2)
    siren = models.CharField(max_length=9)

    def __str__(self):
        return self.name


class Commune(models.Model):
    """
    A French commune
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    departement = models.ForeignKey("Departement", on_delete=models.CASCADE)
    epci = models.ForeignKey("Epci", on_delete=models.CASCADE, null=True)
    insee = models.CharField(max_length=5)
    siren = models.CharField(max_length=9)
    population = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.departement})"
