from django.db import models
from .t_aspic_interco_meta import T302Competences
from .t_aspic_communes import T050Communes
from .t_aspic_other import T090AutresOrganismes

# Tables de liaison
class T301302NjComp(models.Model):
    nature_juridique = models.ForeignKey(
        "T301NaturesJuridiques",
        models.DO_NOTHING,
        db_column="nature_juridique",
        blank=True,
        null=True,
    )
    competence = models.ForeignKey(
        "T302Competences",
        models.DO_NOTHING,
        db_column="competence",
        blank=True,
        null=True,
    )
    dgf_bonifiee = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t301_302_nj_comp"

    def __str__(self):
        return f"{self.nature_juridique} / {self.competence}"


class T301304NjMf(models.Model):
    nature_juridique = models.ForeignKey(
        "T301NaturesJuridiques", models.DO_NOTHING, db_column="nature_juridique"
    )
    mode_financement = models.ForeignKey(
        "T304ModeFinanc", models.DO_NOTHING, db_column="mode_financement"
    )

    class Meta:
        managed = False
        db_table = "t301_304_nj_mf"

    def __str__(self):
        return f"{self.nature_juridique} - {self.mode_financement}"


class T301306NjMr(models.Model):
    nature_juridique = models.ForeignKey(
        "T301NaturesJuridiques", models.DO_NOTHING, db_column="nature_juridique"
    )
    mode_repartition_siege = models.ForeignKey(
        "T306ModeRepartitionSiege",
        models.DO_NOTHING,
        db_column="mode_repartition_siege",
    )

    class Meta:
        managed = False
        db_table = "t301_306_nj_mr"

    def __str__(self):
        return f"{self.nature_juridique} - {self.mode_repartition_siege}"


class T302311CompetencesGroup(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements", models.DO_NOTHING, db_column="groupement", primary_key=True
    )
    competence = models.ForeignKey(
        "T302Competences", models.DO_NOTHING, db_column="competence"
    )
    competence_texte_libre = models.CharField(max_length=26000, blank=True, null=True)
    mode_gestion = models.ForeignKey(
        "T305ModeGestion",
        models.DO_NOTHING,
        db_column="mode_gestion",
        blank=True,
        null=True,
    )
    int_com = models.BooleanField(blank=True, null=True)
    int_com_texte = models.CharField(max_length=7000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t302_311_competences_group"
        unique_together = (("groupement", "competence"),)

    def __str__(self):
        return f"{self.groupement} - {self.competence}"


class T303CompetencesConservAut(models.Model):
    groupement = models.OneToOneField(
        T302311CompetencesGroup,
        models.DO_NOTHING,
        db_column="groupement",
        primary_key=True,
    )
    membre = models.CharField(max_length=9)
    competence = models.ForeignKey(
        T302Competences, models.DO_NOTHING, db_column="competence"
    )

    class Meta:
        managed = False
        db_table = "t303_competences_conserv_aut"
        unique_together = (("groupement", "competence", "membre"),)

    def __str__(self):
        return f"{self.groupement} / {self.competence} / {self.membre}"


class T303CompetencesConservCom(models.Model):
    groupement = models.OneToOneField(
        T302311CompetencesGroup,
        models.DO_NOTHING,
        db_column="groupement",
        primary_key=True,
    )
    membre = models.CharField(max_length=9)
    competence = models.ForeignKey(
        T302Competences, models.DO_NOTHING, db_column="competence"
    )

    class Meta:
        managed = False
        db_table = "t303_competences_conserv_com"
        unique_together = (("groupement", "competence", "membre"),)

    def __str__(self):
        return f"{self.groupement} / {self.competence} / {self.membre}"


class T303CompetencesConservGrp(models.Model):
    groupement = models.OneToOneField(
        T302311CompetencesGroup,
        models.DO_NOTHING,
        db_column="groupement",
        primary_key=True,
    )
    membre = models.CharField(max_length=9)
    competence = models.ForeignKey(
        T302Competences, models.DO_NOTHING, db_column="competence"
    )

    class Meta:
        managed = False
        db_table = "t303_competences_conserv_grp"
        unique_together = (("groupement", "competence", "membre"),)

    def __str__(self):
        return f"{self.groupement} / {self.competence} / {self.membre}"


class T311050CommunesMembres(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements", models.DO_NOTHING, db_column="groupement", primary_key=True
    )
    membre = models.ForeignKey(T050Communes, models.DO_NOTHING, db_column="membre")
    nombre_de_delegues = models.IntegerField(blank=True, null=True)
    nombre_de_delegues_sup = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t311_050_communes_membres"
        unique_together = (("groupement", "membre"),)

    def __str__(self):
        return f"{self.groupement} / {self.membre}"


class T311090AutresOrganismes(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements", models.DO_NOTHING, db_column="groupement", primary_key=True
    )
    membre = models.ForeignKey(
        T090AutresOrganismes, models.DO_NOTHING, db_column="membre"
    )
    nombre_de_delegues = models.IntegerField(blank=True, null=True)
    nombre_de_delegues_sup = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t311_090_autres_organismes"
        unique_together = (("groupement", "membre"),)

    def __str__(self):
        return f"{self.groupement} / {self.membre}"


class T311311GroupementsMembr(models.Model):
    groupement = models.OneToOneField(
        "T311Groupements",
        models.DO_NOTHING,
        db_column="groupement",
        primary_key=True,
        related_name="gm_groupement",
    )
    membre = models.ForeignKey(
        "T311Groupements",
        models.DO_NOTHING,
        db_column="membre",
        related_name="gm_membre",
    )
    nombre_de_delegues = models.IntegerField(blank=True, null=True)
    nombre_de_delegues_sup = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "t311_311_groupements_membr"
        unique_together = (("groupement", "membre"),)

    def __str__(self):
        return f"{self.groupement} / {self.membre}"


class T3115090MembresSubst(models.Model):
    groupement = models.OneToOneField(
        T311311GroupementsMembr,
        models.DO_NOTHING,
        db_column="groupement",
        primary_key=True,
    )
    groupement_par_sub = models.ForeignKey(
        T311050CommunesMembres, models.DO_NOTHING, db_column="groupement_par_sub"
    )
    membre = models.CharField(max_length=9)
    competence = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = "t311_5090_membres_subst"
        unique_together = (
            ("groupement", "membre", "groupement_par_sub", "competence"),
        )

    def __str__(self):
        return f"{self.groupement} / {self.membre} / {self.groupement_par_sub} / {self.competence}"
