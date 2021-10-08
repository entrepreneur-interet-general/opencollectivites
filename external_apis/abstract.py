from django.db import models
from francedata.services.django_admin import TimeStampModel


class ExternalApiQuery(TimeStampModel):
    name = models.CharField(max_length=255, verbose_name="nom", unique=True)
    query = models.CharField(
        max_length=1000,
        verbose_name="requête",
        help_text="Entrer '*' pour rechercher toutes les entrées",
    )

    last_polled = models.DateTimeField(
        blank=True, null=True, verbose_name="dernière tentative"
    )
    last_success = models.DateTimeField(
        blank=True, null=True, verbose_name="dernière réussite"
    )
    last_change = models.DateTimeField(
        blank=True, null=True, verbose_name="dernier changement"
    )
    is_active = models.BooleanField(default=True, verbose_name="requête active")

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.name}"

    def run(self, since: str = "") -> None:
        raise NotImplementedError
