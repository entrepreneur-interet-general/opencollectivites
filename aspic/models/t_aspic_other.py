from django.db import models


class T090AutresOrganismes(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    nom = models.CharField(max_length=255)
    dep = models.CharField(max_length=3)
    cp = models.CharField(max_length=5, blank=True, null=True)
    bd = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t090_autres_organismes"

    def __str__(self):
        return f"{self.nom} ({self.siren})"


class T173DatesDonnees(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t173_dates_donnees"

    def __str__(self):
        return f"{self.code}: {self.libelle}"


class T307Naf(models.Model):
    code = models.CharField(unique=True, max_length=5)
    nom = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t307_naf"

    def __str__(self):
        return f"{self.nom} ({self.code})"
