from django.db import models
from .t_aspic_interco_meta import (
    T301NaturesJuridiques,
    T304ModeFinanc,
    T306ModeRepartitionSiege,
)
from .t_aspic_interco_liaison import (
    T311050CommunesMembres,
    T311311GroupementsMembr,
    T311090AutresOrganismes,
)
from .t_aspic_communes import T050Communes

# Données de base + certaines données de contexte
class T311Groupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    raison_sociale = models.CharField(max_length=512)
    sigle = models.CharField(max_length=160, blank=True, null=True)
    nature_juridique = models.ForeignKey(
        T301NaturesJuridiques, models.DO_NOTHING, db_column="nature_juridique"
    )
    ligne_1 = models.CharField(max_length=255, blank=True, null=True)
    ligne_2 = models.CharField(max_length=255, blank=True, null=True)
    ligne_3 = models.CharField(max_length=255, blank=True, null=True)
    code_postal = models.CharField(max_length=5, blank=True, null=True)
    bureau_distributeur = models.CharField(max_length=50, blank=True, null=True)
    commune_siege = models.ForeignKey(
        T050Communes,
        models.DO_NOTHING,
        db_column="commune_siege",
        related_name="groupement_commune_siege",
    )
    telephone = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    ligne_annexe_1 = models.CharField(max_length=255, blank=True, null=True)
    ligne_annexe_2 = models.CharField(max_length=255, blank=True, null=True)
    ligne_annexe_3 = models.CharField(max_length=255, blank=True, null=True)
    code_postal_annexe = models.CharField(max_length=5, blank=True, null=True)
    bureau_distributeur_annexe = models.CharField(max_length=50, blank=True, null=True)
    telephone_annexe = models.CharField(max_length=14, blank=True, null=True)
    fax_annexe = models.CharField(max_length=14, blank=True, null=True)
    adresse_e_mail = models.CharField(max_length=320, blank=True, null=True)
    adresse_site_internet = models.CharField(max_length=100, blank=True, null=True)
    date_arrete = models.DateField()
    date_effet = models.DateField()
    a_la_carte = models.BooleanField(blank=True, null=True)
    duree_vie = models.IntegerField(blank=True, null=True)
    repartition_siege = models.ForeignKey(
        T306ModeRepartitionSiege, models.DO_NOTHING, db_column="repartition_siege"
    )
    autre_repartition = models.CharField(max_length=1500, blank=True, null=True)
    mode_financ = models.ForeignKey(
        T304ModeFinanc, models.DO_NOTHING, db_column="mode_financ"
    )
    dsc = models.BooleanField(blank=True, null=True)
    reom = models.BooleanField(blank=True, null=True)
    teom = models.BooleanField(blank=True, null=True)
    autre_taxe = models.BooleanField(blank=True, null=True)
    texte_autre_taxe = models.CharField(max_length=255, blank=True, null=True)
    autre_redevance = models.BooleanField(blank=True, null=True)
    texte_autre_redevance = models.CharField(max_length=255, blank=True, null=True)
    dgf_bonifiee = models.BooleanField(blank=True, null=True)
    tresorier_receveur = models.ForeignKey(
        T050Communes,
        models.DO_NOTHING,
        db_column="tresorier_receveur",
        related_name="groupement_tresorier_receveur",
        blank=True,
        null=True,
    )
    nb_tot_del_tit = models.IntegerField(blank=True, null=True)
    nb_tot_del_sup = models.IntegerField(blank=True, null=True)
    nb_tot_vic_pre = models.IntegerField(blank=True, null=True)
    archive = models.BooleanField(blank=True, null=True)
    arret_competences = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t311_groupements"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"

    def list_current_epcis():
        return T311Groupements.objects.filter(
            nature_juridique__fiscalite_propre=True, archive=False
        )


class T315GroupementsSirene(models.Model):
    siren = models.CharField(unique=True, max_length=9)
    raison_sociale = models.CharField(max_length=120)
    no_voie = models.CharField(max_length=4, blank=True, null=True)
    type_voie = models.CharField(max_length=4, blank=True, null=True)
    indice_repetition = models.CharField(max_length=1, blank=True, null=True)
    libelle_voie = models.CharField(max_length=33, blank=True, null=True)
    complement_localisation = models.CharField(max_length=38, blank=True, null=True)
    distribution_speciale = models.CharField(max_length=8, blank=True, null=True)
    code_postal = models.CharField(max_length=5, blank=True, null=True)
    bureau_distributeur = models.CharField(max_length=50, blank=True, null=True)
    code_ape = models.CharField(max_length=5, blank=True, null=True)
    categorie_juridique = models.CharField(max_length=4, blank=True, null=True)
    nom_commune = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t315_groupements_sirene"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


# Données de base sur les EPCI
class T902ColbEpci(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    num_departement = models.CharField(max_length=3)
    nom = models.CharField(max_length=100)
    nj = models.CharField(max_length=5)
    mf = models.CharField(max_length=3)
    nb_com = models.IntegerField(blank=True, null=True)
    pop_tot = models.IntegerField(blank=True, null=True)
    pop_mun = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t902_colb_epci"

    def __str__(self):
        return f"{self.nom} ({self.siren})"


# Données de contexte
class T171DonneesGroupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    code_donnee = models.CharField(max_length=30)
    annee = models.CharField(max_length=4)
    valeur = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t171_donnees_groupements"
        unique_together = (("siren", "code_donnee", "annee"),)

    def __str__(self):
        return f"{self.siren} / {self.code_donnee} / { self.annee}"


class T172PopGroupements(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    pop_tot = models.IntegerField(blank=True, null=True)
    superficie = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t172_pop_groupements"

    def __str__(self):
        return f"{self.siren}"


class T901SspEpci(models.Model):
    siren = models.CharField(primary_key=True, max_length=9)
    num_departement = models.CharField(max_length=3)
    raison_sociale = models.CharField(max_length=50)
    adresse_1 = models.CharField(max_length=50, blank=True, null=True)
    adresse_2 = models.CharField(max_length=50, blank=True, null=True)
    cp_bd = models.CharField(max_length=50)
    code_ape = models.CharField(max_length=5)
    cj = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = "t901_ssp_epci"

    def __str__(self):
        return f"{self.raison_sociale} ({self.siren})"


# Délégués
class T311DeleguesCom(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements", models.DO_NOTHING, db_column="groupement", primary_key=True
    )
    membre = models.CharField(max_length=9, blank=True, null=True)
    civilite = models.CharField(max_length=5, blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    prenom = models.CharField(max_length=50, blank=True, null=True)
    fonction = models.CharField(max_length=20, blank=True, null=True)
    statut = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t311_delegues_com"

    def __str__(self):
        return f"{self.groupement} - {self.membre} - {self.civilite} {self.prenom} {self.nom} ({self.fonction})"


class T312DeleguesGrp(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements", models.DO_NOTHING, db_column="groupement", primary_key=True
    )
    membre = models.CharField(max_length=9, blank=True, null=True)
    civilite = models.CharField(max_length=5, blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    prenom = models.CharField(max_length=50, blank=True, null=True)
    fonction = models.CharField(max_length=20, blank=True, null=True)
    statut = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t312_delegues_grp"

    def __str__(self):
        return f"{self.groupement} - {self.membre} - {self.civilite} {self.prenom} {self.nom} ({self.fonction})"


class T313DeleguesAut(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements", models.DO_NOTHING, db_column="groupement", primary_key=True
    )
    membre = models.CharField(max_length=9, blank=True, null=True)
    civilite = models.CharField(max_length=5, blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    prenom = models.CharField(max_length=50, blank=True, null=True)
    fonction = models.CharField(max_length=20, blank=True, null=True)
    statut = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t313_delegues_aut"

    def __str__(self):
        return f"{self.groupement} - {self.membre} - {self.civilite} {self.prenom} {self.nom} ({self.fonction})"
