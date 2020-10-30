from django.db import models


class Topic(models.Model):
    """
    (fr: Thématique)
    The main topic of a site or document. Used for filtering.
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name
