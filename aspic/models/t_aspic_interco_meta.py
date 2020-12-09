from django.db import models

# Métadonnées
class T301NaturesJuridiques(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    fiscalite_propre = models.BooleanField(blank=True, null=True)
    syndicat_carte = models.BooleanField(blank=True, null=True)
    annee_creation = models.CharField(max_length=4, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t301_natures_juridiques"

    def __str__(self):
        return f"{self.code}"


class T3020CatCompet(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    nom = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "t3020_cat_compet"

    def __str__(self):
        return f"{self.code}"


class T302Competences(models.Model):
    code = models.CharField(primary_key=True, max_length=4)
    nom = models.CharField(max_length=512)
    cat = models.ForeignKey(T3020CatCompet, models.DO_NOTHING, db_column="cat")

    class Meta:
        managed = False
        db_table = "t302_competences"

    def __str__(self):
        return f"{self.nom} ({self.code})"


class T304ModeFinanc(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    fiscalite_propre = models.BooleanField(blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t304_mode_financ"

    def __str__(self):
        return f"{self.libelle} ({self.code})"


class T305ModeGestion(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t305_mode_gestion"

    def __str__(self):
        return f"{self.libelle} ({self.code})"


class T306ModeRepartitionSiege(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    ordre_affichage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t306_mode_repartition_siege"

    def __str__(self):
        return f"{self.libelle} ({self.code})"
