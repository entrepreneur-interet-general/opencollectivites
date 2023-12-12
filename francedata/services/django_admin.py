"""
A meta model with a collection of related admin tools.
"""
from django.db import models
from django.contrib import admin
from django.db.models.base import Model
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.apps import apps

from django.shortcuts import resolve_url
from django.utils.safestring import SafeText
from django.contrib.admin.templatetags.admin_urls import admin_urlname


class TimeStampModel(models.Model):
    """
    Meta model with timestamps fields for creation and last update dates.
    """

    created_at = models.DateTimeField("date de création", auto_now_add=True)
    updated_at = models.DateTimeField("date de modification", auto_now=True)

    class Meta:
        ordering = ["created_at"]
        abstract = True


class TimeStampModelAdmin(admin.ModelAdmin):
    """
    Meta admin for the TimeStampModel
    """

    readonly_fields = ["id", "created_at", "updated_at"]

    class Meta:
        abstract = True

def add_current_datayear(modeladmin, request, queryset):
    """
    Marks the collectivity as belonging to the current year
    """
    for entry in queryset:
        entry.add_current_datayear()
        entry.save()

add_current_datayear.short_description = 'Ajouter le millésime actuel'


class CollectivityModelAdmin(TimeStampModelAdmin):
    """
    Specific TimeStampModelAdmin for collectivity models
    """
    actions = [add_current_datayear, ]

    class Meta:
        abstract = True


def view_reverse_changelink(
    obj: Model,
    module_name: str,
    local_model_name: str,
    distant_model_name: str,
    key: int = "pk",
) -> str:
    """
    Generates a link to the list of related items of a many-to-many field,
    for use in the admin list and change views.
    """

    distant_model = apps.get_model(module_name, distant_model_name)
    count = getattr(obj, f"{distant_model_name}_set").count()
    url = (
        reverse(f"admin:{module_name}_{distant_model_name}_changelist")
        + "?"
        + urlencode({f"{local_model_name}__id__exact": f"{getattr(obj, key)}"})
    )
    if count <= 1:
        label = f"{count} {getattr(distant_model._meta, 'verbose_name')}"
    else:
        label = f"{count} {getattr(distant_model._meta, 'verbose_name_plural')}"
    return format_html('<a href="{}">{}</a>', url, label)


def related_object_link(obj: Model, name: str = None) -> str:
    """
    Generates a link to the selected value for a foreign key, for use in the admin change view.
    """
    url = resolve_url(admin_urlname(obj._meta, SafeText("change")), obj.pk)
    if not name:
        name = str(obj)
    return format_html(f'<a href="{url}">{name}</a>')
