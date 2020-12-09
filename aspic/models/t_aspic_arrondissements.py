from django.db import models
from .t_aspic_departements import T009Departements

# Données de base
class T010Arrondissements(models.Model):
    num_departement = models.ForeignKey(
        T009Departements, models.DO_NOTHING, db_column="num_departement"
    )
    dep = models.CharField(max_length=2)
    ard = models.CharField(max_length=1)
    nom = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "t010_arrondissements"
        unique_together = (("num_departement", "ard"),)

    def __str__(self):
        return f"{self.nom} ({self.num_departement} - {self.ard})"


# Données de contexte
class T110DonneesArrondissements(models.Model):
    num_departement = models.CharField(primary_key=True, max_length=3)
    ard = models.CharField(max_length=1)
    code_donnee = models.CharField(max_length=30)
    annee = models.CharField(max_length=4)
    valeur = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t110_donnees_arrondissements"
        unique_together = (("num_departement", "ard", "code_donnee", "annee"),)

    def __str__(self):
        return (
            f"{self.num_departement} / {self.ard} / {self.code_donnee} / {self.annee}"
        )