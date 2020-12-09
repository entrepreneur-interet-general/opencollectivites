from django.db import models
from .t_aspic_regions import T008Regions


class T009Departements(models.Model):
    num_departement = models.CharField(primary_key=True, max_length=3)
    dep = models.CharField(max_length=3)
    region = models.ForeignKey(T008Regions, models.DO_NOTHING, db_column="region")
    nom = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "t009_departements"

    def __str__(self):
        return f"{self.nom} ({self.num_departement})"


class T109DonneesDepartements(models.Model):
    num_departement = models.CharField(primary_key=True, max_length=3)
    code_donnee = models.CharField(max_length=30)
    annee = models.CharField(max_length=4)
    valeur = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t109_donnees_departements"
        unique_together = (("num_departement", "code_donnee", "annee"),)

    def __str__(self):
        return f"{self.num_departement} / {self.code_donnee} / { self.annee}"
