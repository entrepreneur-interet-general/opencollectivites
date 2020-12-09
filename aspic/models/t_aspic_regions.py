from django.db import models


class T008Regions(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    nom = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "t008_regions"

    def __str__(self):
        return f"{self.nom} ({self.code})"
