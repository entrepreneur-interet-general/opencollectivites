from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from francedata.services.django_admin import (
    TimeStampModelAdmin,
    view_reverse_changelink,
)

from bnsp import models

# Register your models here.


@admin.register(models.Query)
class QueryAdmin(TimeStampModelAdmin):
    search_fields = ("name", "query")
    list_display = (
        "__str__",
        "last_polled",
        "view_documents_link",
    )
    list_filter = ("source",)

    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
        "view_documents_link",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    ("query", "live"),
                    "source",
                    "view_documents_link",
                ]
            },
        ),
        (
            "Exécution",
            {
                "fields": [
                    "last_polled",
                    "last_success",
                    "last_change",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "bnsp_query", "document")

    view_documents_link.short_description = "Documents"
