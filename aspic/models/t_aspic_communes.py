from django.db import models

from .t_aspic_departements import T009Departements


# Données de base
class T050Communes(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    num_departement = models.ForeignKey(
        T009Departements, models.DO_NOTHING, db_column="num_departement"
    )
    dep = models.CharField(max_length=2)
    ard = models.CharField(max_length=1)
    can = models.CharField(max_length=2)
    cod = models.CharField(max_length=3)
    nom = models.CharField(max_length=80)
    civ_maire = models.CharField(max_length=5, blank=True, null=True)
    pre_maire = models.CharField(max_length=50, blank=True, null=True)
    nom_maire = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t050_communes"
        unique_together = (("dep", "cod"),)

    def __str__(self):
        return f"{self.nom} ({self.dep}{self.cod})"


# Données de contexte
class T051Recensements(models.Model):
    siren = models.OneToOneField(
        T050Communes, models.DO_NOTHING, db_column="siren", primary_key=True
    )
    annee = models.CharField(max_length=4)
    pop_tot = models.IntegerField(blank=True, null=True)
    pop_mun = models.IntegerField(blank=True, null=True)
    pop_sdc = models.IntegerField(blank=True, null=True)
    dernier = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t051_recensements"
        unique_together = (("siren", "annee"),)

    def __str__(self):
        return f"{self.siren} ({self.annee})"


class T052AdressesCommunes(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    mairie = models.CharField(max_length=15, blank=True, null=True)
    adresse_1 = models.CharField(max_length=100, blank=True, null=True)
    adresse_2 = models.CharField(max_length=100, blank=True, null=True)
    adresse_3 = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=5, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True)
    e_mail = models.CharField(max_length=320, blank=True, null=True)
    nomuu = models.CharField(max_length=100, blank=True, null=True)
    nomau = models.CharField(max_length=100, blank=True, null=True)
    nombv = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t052_adresses_communes"

    def __str__(self):
        return f"{self.ville} ({self.code_postal})"


class T150DonneesCommunes(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    code_donnee = models.CharField(max_length=30)
    annee = models.CharField(max_length=4)
    valeur = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t150_donnees_communes"
        unique_together = (("siren", "code_donnee", "annee"),)

    def __str__(self):
        return f"{self.siren} / {self.code_donnee} / {self.annee}"
