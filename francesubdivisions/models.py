from django.db import models


class Region(models.Model):
    """
    A French région
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    insee = models.CharField(max_length=2)
    siren = models.CharField(max_length=9)


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
