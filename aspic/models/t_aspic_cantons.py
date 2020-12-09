from django.db import models
from .t_aspic_departements import T009Departements

# Données de base
class T011Cantons(models.Model):
    num_departement = models.ForeignKey(
        T009Departements, models.DO_NOTHING, db_column="num_departement"
    )
    dep = models.CharField(max_length=2)
    ard = models.CharField(max_length=1)
    can = models.CharField(max_length=2)
    nom = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "t011_cantons"
        unique_together = ("num_departement", "ard", "can")

    def __str__(self):
        return f"{self.nom} ({self.num_departement} - {self.ard} - {self.can})"


# Données de contexte
class T111DonneesCantons(models.Model):
    num_departement = models.CharField(primary_key=True, max_length=3)
    ard = models.CharField(max_length=1)
    can = models.CharField(max_length=2)
    code_donnee = models.CharField(max_length=30)
    annee = models.CharField(max_length=4)
    valeur = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t111_donnees_cantons"
        unique_together = (("num_departement", "ard", "can", "code_donnee", "annee"),)

    def __str__(self):
        return f"{self.num_departement} / {self.ard} / {self.can} / {self.code_donnee} / {self.annee}"
