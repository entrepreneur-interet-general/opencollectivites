from django.db import models
from .t_aspic_intercommunalites import T311Groupements
from .t_aspic_departements import T009Departements


class T320CategorieOperation(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    nom = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t320_categorie_operation"

    def __str__(self):
        return f"{self.nom} ({self.code})"


class T321CategorieEvenement(models.Model):
    code_operation = models.OneToOneField(
        T320CategorieOperation,
        models.DO_NOTHING,
        db_column="code_operation",
        primary_key=True,
    )
    code = models.CharField(max_length=8)
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t321_categorie_evenement"
        unique_together = (("code_operation", "code"),)

    def __str__(self):
        return f"{self.code_operation} ({self.code})"


class T322Operations(models.Model):
    groupement = models.ForeignKey(
        T311Groupements, models.DO_NOTHING, db_column="groupement"
    )
    categorie = models.ForeignKey(
        T320CategorieOperation, models.DO_NOTHING, db_column="categorie"
    )
    date = models.DateField(blank=True, null=True)
    date_effet = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=7000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t322_operations"

    def __str__(self):
        return f"{self.groupement} - {self.categorie}"


class T323Evenements(models.Model):
    groupement = models.ForeignKey(
        T311Groupements, models.DO_NOTHING, db_column="groupement"
    )
    categorie_operation = models.ForeignKey(
        T321CategorieEvenement, models.DO_NOTHING, db_column="categorie_operation"
    )
    categorie_evenement = models.CharField(max_length=8)
    operation = models.ForeignKey(
        T322Operations, models.DO_NOTHING, db_column="operation"
    )
    date = models.DateField(blank=True, null=True)
    date_effet = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=7000, blank=True, null=True)
    visible_consultation = models.BooleanField(blank=True, null=True)
    url_recueil_acte = models.CharField(max_length=1200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t323_evenements"

    def __str__(self):
        return f"{self.groupement} - {self.categorie_operation} - {self.categorie_evenement} - {self.operation}"


class T324Documents(models.Model):
    groupement = models.ForeignKey(
        T311Groupements, models.DO_NOTHING, db_column="groupement"
    )
    operation = models.ForeignKey(
        T322Operations, models.DO_NOTHING, db_column="operation"
    )
    titre = models.CharField(max_length=1000, blank=True, null=True)
    type_mime = models.CharField(max_length=50, blank=True, null=True)
    contenu = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_creation = models.DateField(blank=True, null=True)
    date_derniere_maj = models.DateField(blank=True, null=True)
    taille = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t324_documents"

    def __str__(self):
        return f"{self.groupement} - {self.operation} - {self.titre}"


class T326Archive(models.Model):
    departement_siege = models.OneToOneField(
        T009Departements,
        models.DO_NOTHING,
        db_column="departement_siege",
        primary_key=True,
    )
    nouveau_siren = models.ForeignKey(
        T311Groupements, models.DO_NOTHING, db_column="nouveau_siren"
    )
    ancien_siren = models.CharField(max_length=9)
    code_operation = models.ForeignKey(
        T320CategorieOperation, models.DO_NOTHING, db_column="code_operation"
    )
    date_creation = models.DateTimeField()
    texte_ancien_groupement = models.CharField(
        max_length=4000000, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t326_archive"
        unique_together = (
            (
                "departement_siege",
                "nouveau_siren",
                "ancien_siren",
                "code_operation",
                "date_creation",
            ),
        )

    def __str__(self):
        return (
            f"{self.departement_siege} - {self.nouveau_siren} - {self.code_operation}"
        )
