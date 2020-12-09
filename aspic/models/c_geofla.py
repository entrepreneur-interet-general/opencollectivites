from django.db import models

#########################################
# Tables géographiques
#########################################


class C008Regions(models.Model):
    code_reg = models.CharField(max_length=2, primary_key=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c008_regions"

    def __str__(self):
        return f"{self.nom_region} ({self.code_reg})"


class C009Departements(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_chf = models.CharField(max_length=3, blank=True, null=True)
    nom_chf = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c009_departements"

    def __str__(self):
        return f"{self.nom_dept} ({self.code_dept})"


# Tables géographiques pour les communes
class C050Communes(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_comm = models.CharField(max_length=3, blank=True, null=True)
    insee_com = models.CharField(max_length=5, blank=True, null=True)
    nom_comm = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    z_moyen = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    code_cant = models.CharField(max_length=2, blank=True, null=True)
    code_arr = models.CharField(max_length=1, blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c050_communes"

    def __str__(self):
        return f"{self.nom_comm} ({self.insee_com})"


# Tables géographiques pour la Guadeloupe
class C971Communes(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_comm = models.CharField(max_length=3, blank=True, null=True)
    insee_com = models.CharField(max_length=5, blank=True, null=True)
    nom_comm = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    z_moyen = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    code_cant = models.CharField(max_length=2, blank=True, null=True)
    code_arr = models.CharField(max_length=1, blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c971_communes"

    def __str__(self):
        return f"{self.nom_comm} ({self.insee_com})"


class C972Communes(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_comm = models.CharField(max_length=3, blank=True, null=True)
    insee_com = models.CharField(max_length=5, blank=True, null=True)
    nom_comm = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    z_moyen = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    code_cant = models.CharField(max_length=2, blank=True, null=True)
    code_arr = models.CharField(max_length=1, blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c972_communes"

    def __str__(self):
        return f"{self.nom_comm} ({self.insee_com})"


class C973Communes(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_comm = models.CharField(max_length=3, blank=True, null=True)
    insee_com = models.CharField(max_length=5, blank=True, null=True)
    nom_comm = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    z_moyen = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    code_cant = models.CharField(max_length=2, blank=True, null=True)
    code_arr = models.CharField(max_length=1, blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c973_communes"

    def __str__(self):
        return f"{self.nom_comm} ({self.insee_com})"


class C974Communes(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_comm = models.CharField(max_length=3, blank=True, null=True)
    insee_com = models.CharField(max_length=5, blank=True, null=True)
    nom_comm = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    z_moyen = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    code_cant = models.CharField(max_length=2, blank=True, null=True)
    code_arr = models.CharField(max_length=1, blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c974_communes"

    def __str__(self):
        return f"{self.nom_comm} ({self.insee_com})"


class C976Communes(models.Model):
    gid = models.AutoField(primary_key=True)
    id_geofla = models.IntegerField(blank=True, null=True)
    code_comm = models.CharField(max_length=3, blank=True, null=True)
    insee_com = models.CharField(max_length=5, blank=True, null=True)
    nom_comm = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    x_chf_lieu = models.IntegerField(blank=True, null=True)
    y_chf_lieu = models.IntegerField(blank=True, null=True)
    x_centroid = models.IntegerField(blank=True, null=True)
    y_centroid = models.IntegerField(blank=True, null=True)
    z_moyen = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    code_cant = models.CharField(max_length=2, blank=True, null=True)
    code_arr = models.CharField(max_length=1, blank=True, null=True)
    code_dept = models.CharField(max_length=2, blank=True, null=True)
    nom_dept = models.CharField(max_length=30, blank=True, null=True)
    code_reg = models.CharField(max_length=2, blank=True, null=True)
    nom_region = models.CharField(max_length=50, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry

    class Meta:
        managed = False
        db_table = "c976_communes"

    def __str__(self):
        return f"{self.nom_comm} ({self.insee_com})"


# Tables géographiques pour les intercommunalités
class C311Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry.
    centroid = models.TextField(blank=True, null=True)  # Geometry.

    class Meta:
        managed = False
        db_table = "c311_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


class C971Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry.
    centroid = models.TextField(blank=True, null=True)  # Geometry.

    class Meta:
        managed = False
        db_table = "c971_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


class C972Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry.
    centroid = models.TextField(blank=True, null=True)  # Geometry.

    class Meta:
        managed = False
        db_table = "c972_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


class C973Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry.
    centroid = models.TextField(blank=True, null=True)  # Geometry.

    class Meta:
        managed = False
        db_table = "c973_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


class C974Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry.
    centroid = models.TextField(blank=True, null=True)  # Geometry.

    class Meta:
        managed = False
        db_table = "c974_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


class C976Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # Geometry.
    centroid = models.TextField(blank=True, null=True)  # Geometry.

    class Meta:
        managed = False
        db_table = "c976_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


# Table vide
"""
class C312GroupementsTous(models.Model):
    siren = models.CharField(max_length=9)
    raison_sociale = models.CharField(max_length=100)
    sigle = models.CharField(max_length=100, blank=True, null=True)
    nature_juridique = models.CharField(max_length=5)
    mode_financ = models.CharField(max_length=5)
    dep_siege = models.CharField(max_length=3, blank=True, null=True)
    commune_siege = models.CharField(max_length=3, blank=True, null=True)
    population = models.FloatField(blank=True, null=True)
    nb_communes = models.IntegerField(blank=True, null=True)
    nb_competences = models.IntegerField(blank=True, null=True)
    competences = models.TextField(blank=True, null=True)  # This field type is a guess.
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    centroid = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "c312_groupements_tous"
#"""