from django.db import models

###############################################
# Tables décrivant le contenu d'autres tables
###############################################


class R009Departements(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "r009_departements"

    def __str__(self):
        return f"{code}"


class R010Arrondissements(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "r010_arrondissements"

    def __str__(self):
        return f"{code}"


class R011Cantons(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "r011_cantons"

    def __str__(self):
        return f"{code}"


class R050Communes(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "r050_communes"

    def __str__(self):
        return f"{code}"


class R311Groupements(models.Model):
    code = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "r311_groupements"

    def __str__(self):
        return f"{code}"