from django.db import models
from django.contrib import admin, messages
from django.http.response import HttpResponseRedirect
from django.utils.translation import ngettext

from django_json_widget.widgets import JSONEditorWidget
from francedata.services.django_admin import (
    TimeStampModelAdmin,
    view_reverse_changelink,
)
from simple_history.admin import SimpleHistoryAdmin
from external_apis.models import (
    DataMapping,
    OpenDataSoftEndpoint,
    OpenDataSoftQuery,
    BnspQuery,
)


@admin.register(DataMapping)
class DataMappingAdmin(SimpleHistoryAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(OpenDataSoftEndpoint)
class OpenDataSoftEndpointAdmin(TimeStampModelAdmin):
    pass


@admin.register(OpenDataSoftQuery)
class OpenDataSoftQueryAdmin(TimeStampModelAdmin):
    change_form_template = "external_apis/admin/query_changeform.html"

    search_fields = ("name", "query")
    list_display = (
        "__str__",
        "last_polled",
        "view_documents_link",
    )
    list_filter = ("endpoint",)

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
                    ("query", "is_active"),
                    "endpoint",
                    "view_documents_link",
                ]
            },
        ),
        (
            "Ajout de métadonnées",
            {
                "fields": [
                    "mapping",
                    "identify_regions",
                    "identify_departements",
                    "identify_metropoles",
                    "identify_years",
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

    actions = ["force_run_queries"]

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "ods_queries", "document")

    view_documents_link.short_description = "Documents"

    # Force immediate execution of query on the admin detail view
    def response_change(self, request, obj):
        if "_force_run_query" in request.POST:
            obj.run()
            return HttpResponseRedirect(".")  # stay on the same detail page
        return super().response_change(request, obj)

    # Force immediate execution of queries on the admin list view
    @admin.action(description="Lancer les requêtes maintenant")
    def force_run_queries(self, request, queryset):
        for q in queryset:
            q.run()

        updated = len(queryset)

        self.message_user(
            request,
            ngettext(
                "%d requête a été exécutée avec succès.",
                "%d requêtes ont été exécutées avec succès.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(BnspQuery)
class BnspQueryAdmin(TimeStampModelAdmin):
    change_form_template = "external_apis/admin/query_changeform.html"

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
                    ("query", "is_active"),
                    "source",
                    "view_documents_link",
                ]
            },
        ),
        (
            "Ajout de métadonnées",
            {
                "fields": [
                    "identify_regions",
                    "identify_departements",
                    "identify_metropoles",
                    "identify_main_cities",
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

    actions = ["force_run_queries"]

    def view_documents_link(self, obj):
        return view_reverse_changelink(obj, "core", "bnsp_queries", "document")

    view_documents_link.short_description = "Documents"

    # Force immediate execution of query on the admin detail view
    def response_change(self, request, obj):
        if "_force_run_query" in request.POST:
            obj.run()
            return HttpResponseRedirect(".")  # stay on the same detail page
        return super().response_change(request, obj)

    # Force immediate execution of queries on the admin list view
    @admin.action(description="Lancer les requêtes maintenant")
    def force_run_queries(self, request, queryset):
        for q in queryset:
            q.run()

        updated = len(queryset)

        self.message_user(
            request,
            ngettext(
                "%d requête a été exécutée avec succès.",
                "%d requêtes ont été exécutées avec succès.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
