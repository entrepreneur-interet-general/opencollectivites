from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from francedata.services.django_admin import (
    TimeStampModelAdmin,
    view_reverse_changelink,
)
from core import models
from config.settings import FRONT_HOME_URL

# Admin methods
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


make_published.short_description = "Marquer la sélection comme publiée"


def make_not_published(modeladmin, request, queryset):
    queryset.update(is_published=False)


make_not_published.short_description = "Marquer la sélection comme non publiée"

# Admin panels
@admin.register(models.Metadata)
class MetadataAdmin(TimeStampModelAdmin):
    list_display = ("prop", "value")


@admin.register(models.DataYear)
class DataYearAdmin(TimeStampModelAdmin):
    pass


@admin.register(models.Scope)
class ScopeAdmin(TimeStampModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "view_sources_link", "view_documents_link")
    ordering = ["name"]

    def view_sources_link(self, obj):
        return view_reverse_changelink(obj, "core", "scope", "source")

    view_sources_link.short_description = "Sources"

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "scope", "document")

    view_documents_link.short_description = "Documents"


@admin.register(models.DocumentType)
class DocumentTypeAdmin(TimeStampModelAdmin):
    list_display = ("name", "view_documents_link", "view_logo")
    ordering = ["name"]

    def view_logo(self, obj):
        logo_full_url = f"{FRONT_HOME_URL}{obj.icon_path}"
        return format_html(f'<img src="{logo_full_url}" alt="" />')

    view_logo.short_description = "Logo"

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "document_type", "document")

    view_documents_link.short_description = "Documents"


@admin.register(models.Topic)
class TopicAdmin(TimeStampModelAdmin):
    list_display = ("name", "view_sources_link", "view_documents_link", "view_logo")
    readonly_fields = [
        "view_logo",
        "created_at",
        "updated_at",
    ]
    ordering = ["name"]

    def view_sources_link(self, obj):
        return view_reverse_changelink(obj, "core", "topics", "source")

    view_sources_link.short_description = "Sources"

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "topics", "document")

    def view_logo(self, obj):
        logo_full_url = f"{FRONT_HOME_URL}{obj.icon_path}"
        return format_html(f'<img src="{logo_full_url}" alt="" />')

    view_logo.short_description = "Logo"

    view_documents_link.short_description = "Documents"


@admin.register(models.Organization)
class OrganizationAdmin(TimeStampModelAdmin):
    list_display = ("__str__", "acronym", "name")


@admin.register(models.PageType)
class PageTypeAdmin(TimeStampModelAdmin):
    list_display = ("name", "view_documents_link")

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "publication_pages", "document")

    view_documents_link.short_description = "Documents"


@admin.register(models.Document)
class DocumentAdmin(TimeStampModelAdmin):
    ordering = ("-created_at",)
    search_fields = ("title", "url")
    list_display = (
        "__str__",
        "is_published",
        "last_update",
        "view_thumbnail",
    )
    list_filter = (
        "is_published",
        "source__editor",
        "source",
        "tags",
        ("image_url", admin.EmptyFieldListFilter),
    )

    raw_id_fields = ("epcis", "communes")

    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("title", "is_published"),
                    ("url", "base_domain"),
                ]
            },
        ),
        (
            "Contenu",
            {
                "fields": [
                    "body",
                    ("image_url", "view_image"),
                ]
            },
        ),
        (
            "Source",
            {
                "fields": [
                    "source",
                    "bnsp_queries",
                    "ods_queries",
                ]
            },
        ),
        (
            "Classement",
            {
                "fields": [
                    "weight",
                    "tags",
                    "publication_pages",
                    "years",
                    "scope",
                    "regions",
                    "departements",
                    "epcis",
                    "communes",
                    "topics",
                    "document_type",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]

    readonly_fields = [
        "id",
        "view_image",
        "base_domain",
        "created_at",
        "updated_at",
    ]

    actions = [make_published, make_not_published]

    def view_image(self, obj):
        return format_html(f'<img src="{obj.image_url}" width="300px" alt="" />')

    view_image.short_description = "Image"

    def view_thumbnail(self, obj):
        return format_html(f'<img src="{obj.image_url}" width="40px" alt="" />')

    view_thumbnail.short_description = "Image"


@admin.register(models.Source)
class SourceAdmin(TimeStampModelAdmin):
    search_fields = ("title", "url")
    list_display = (
        "__str__",
        "last_update",
        "view_documents_link",
    )
    list_filter = (
        "source_type",
        "editor",
    )
    raw_id_fields = ("epcis", "communes")

    readonly_fields = [
        "base_domain",
        "created_at",
        "updated_at",
    ]

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "source", "document")

    view_documents_link.short_description = "Documents"
