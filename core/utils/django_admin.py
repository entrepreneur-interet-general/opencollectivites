from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.apps import apps


class TimeStampModel(models.Model):
    created_at = models.DateTimeField("date de création", auto_now_add=True)
    updated_at = models.DateTimeField("date de modification", auto_now=True)

    class Meta:
        ordering = ["created_at"]
        abstract = True


class TimeStampModelAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]

    class Meta:
        abstract = True


def view_reverse_changelink(
    obj, module_name, local_model_name, distant_model_name, key="pk"
):

    distant_model = apps.get_model(module_name, distant_model_name)
    count = getattr(obj, f"{distant_model_name}_set").count()
    url = (
        reverse(f"admin:{module_name}_{distant_model_name}_changelist")
        + "?"
        + urlencode({f"{local_model_name}__id": f"{getattr(obj, key)}"})
    )
    if count <= 1:
        label = f"{count} {getattr(distant_model._meta, 'verbose_name')}"
    else:
        label = f"{count} {getattr(distant_model._meta, 'verbose_name_plural')}"
    return format_html('<a href="{}">{}</a>', url, label)