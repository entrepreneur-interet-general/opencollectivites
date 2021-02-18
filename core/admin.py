from django.contrib import admin
from django.utils.http import urlencode
from django.utils.html import format_html
from django.urls import reverse

from core.utils.django_admin import TimeStampModelAdmin, view_reverse_changelink
from core import models
from config.settings import FRONT_HOME_URL


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
    list_display = ("name", "view_documents_link")
    ordering = ["name"]

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "documenttype", "document")

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
    pass


@admin.register(models.Document)
class DocumentAdmin(TimeStampModelAdmin):
    search_fields = ("title", "url")
    list_display = ("__str__", "is_published", "last_update", "view_rss_post_link")
    list_filter = ("is_published", "source__editor", "source")

    raw_id_fields = ("rss_post", "epcis", "communes")

    fields = (
        "title",
        "url",
        "base_domain",
        "source",
        "is_published",
        "rss_post",
        "body",
        "publication_pages",
        "scope",
        "regions",
        "departements",
        "epcis",
        "communes",
        "topics",
        "document_type",
        "last_update",
        "created_at",
        "updated_at",
    )

    readonly_fields = [
        "base_domain",
        "view_rss_post_link",
        "created_at",
        "updated_at",
    ]

    def view_rss_post_link(self, obj):
        if obj.rss_post:
            url = reverse("admin:feeds_post_change", args=(obj.rss_post.pk,))
            return format_html('<a href="{}">Post</a>', url)
        else:
            return ""

    view_rss_post_link.short_description = "Lien post associé"


@admin.register(models.Source)
class SourceAdmin(TimeStampModelAdmin):
    search_fields = ("title", "url")
    list_display = (
        "__str__",
        "last_update",
        "view_rss_feed_link",
        "view_documents_link",
    )
    list_filter = (
        "source_type",
        "editor",
    )
    raw_id_fields = ("rss_feed", "epcis", "communes")

    readonly_fields = [
        "base_domain",
        "created_at",
        "updated_at",
    ]

    def view_rss_feed_link(self, obj):
        if obj.rss_feed:
            url = reverse("admin:feeds_source_change", args=(obj.rss_feed.pk,))
            return format_html('<a href="{}">Flux</a>', url)
        else:
            return ""

    view_rss_feed_link.short_description = "Lien flux associé"

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "source", "document")

    view_documents_link.short_description = "Documents"
