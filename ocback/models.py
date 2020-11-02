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


class Scope(models.Model):
    """
    (fr: Portée)
    The reach of a site or document (national, regional, etc.)
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name


class Editor(models.Model):
    """
    (fr: Éditeur)
    The editor of a site or document
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="logos")

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name


class Platform(models.Model):
    """
    (fr:Plateforme)
    A website.
    """

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    editor = models.ForeignKey("Editor", on_delete=models.SET_NULL, null=True)
    rssfeed = models.ForeignKey("feeds.Source", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name
