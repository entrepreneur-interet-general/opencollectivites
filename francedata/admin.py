from django.db.models import JSONField
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django_json_widget.widgets import JSONEditorWidget
from simple_history.admin import SimpleHistoryAdmin

from francedata import models
from francedata.services.django_admin import (
    CollectivityModelAdmin,
    TimeStampModelAdmin,
    related_object_link,
    view_reverse_changelink,
)

# Inlines
class RegionDataInline(admin.TabularInline):
    model = models.RegionData
    extra = 0


class DepartementDataInline(admin.TabularInline):
    model = models.DepartementData
    extra = 0


class EpciDataInline(admin.TabularInline):
    model = models.EpciData
    extra = 0


class CommuneDataInline(admin.TabularInline):
    model = models.CommuneData
    extra = 0


# Templates
@admin.register(models.Region)
class RegionAdmin(CollectivityModelAdmin):
    search_fields = ("name__startswith", "slug", "insee", "siren")
    list_display = ("name", "slug", "insee", "siren", "view_departements_link")
    ordering = ["name"]
    inlines = [RegionDataInline]

    def view_departements_link(self, obj):
        return view_reverse_changelink(obj, "francedata", "region", "departement")

    view_departements_link.short_description = "Départements"

    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "view_departements_link",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "category",
                    "years",
                    "insee",
                    "siren",
                    "view_departements_link",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]


@admin.register(models.Departement)
class DepartementAdmin(CollectivityModelAdmin):
    search_fields = ("name__startswith", "slug", "insee", "siren")
    list_display = ("name", "slug", "insee", "siren", "view_communes_link")
    list_filter = ("years", "region")
    ordering = ["name"]
    inlines = [DepartementDataInline]

    def view_communes_link(self, obj):
        return view_reverse_changelink(obj, "francedata", "departement", "commune")

    view_communes_link.short_description = "Communes"

    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "region_link",
        "view_communes_link",
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "category",
                    "years",
                    "insee",
                    "siren",
                    ("region", "region_link"),
                    "view_communes_link",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]

    def region_link(self, obj):
        return related_object_link(obj.region)

    region_link.short_description = "lien"


@admin.register(models.Epci)
class EpciAdmin(TimeStampModelAdmin):
    search_fields = ("name", "slug", "siren")
    list_display = ("name", "slug", "siren", "view_communes_link")
    ordering = ["name"]
    inlines = [EpciDataInline]

    def view_communes_link(self, obj):
        return view_reverse_changelink(obj, "francedata", "epci", "commune")

    view_communes_link.short_description = "Communes"

    readonly_fields = ["id", "slug", "created_at", "updated_at", "view_communes_link"]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "epci_type",
                    "years",
                    "siren",
                    "view_communes_link",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]


@admin.register(models.Commune)
class CommuneAdmin(TimeStampModelAdmin):
    search_fields = ("name", "slug", "insee", "siren")
    list_display = ("name", "slug", "insee", "siren")
    list_filter = ("years", "departement", "epci")
    ordering = ["name", "insee"]
    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "epci_link",
        "departement_link",
        "region_link",
    ]
    inlines = [CommuneDataInline]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "population",
                    "years",
                    "insee",
                    "siren",
                    ("departement", "departement_link", "region_link"),
                    ("epci", "epci_link"),
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]

    def epci_link(self, obj):
        return related_object_link(obj.epci)

    epci_link.short_description = "lien"

    def departement_link(self, obj):
        return related_object_link(obj.departement)

    departement_link.short_description = "département"

    def region_link(self, obj):
        return related_object_link(obj.departement.region)

    region_link.short_description = "région"


@admin.register(models.DataSource)
class DataSourceAdmin(TimeStampModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "public_label",
                    "url",
                    "year",
                ]
            },
        ),
        ("Métadonnées", {"fields": ["id", "created_at", "updated_at"]}),
    ]
    list_filter = ("title", "year")


@admin.register(models.DataSourceFile)
class DataSourceFileAdmin(TimeStampModelAdmin):
    change_form_template = "desl_imports/admin/query_changeform.html"

    # Import the file data from the admin detail view
    def response_change(self, request, obj):
        if "_import_file_data" in request.POST:
            obj.import_file_data_command(request)
            return HttpResponseRedirect(".")  # stay on the same detail page
        return super().response_change(request, obj)

    list_display = ("__str__", "is_imported")


@admin.register(models.DataMapping)
class DataMappingAdmin(SimpleHistoryAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


admin.site.register(models.Metadata)
admin.site.register(models.DataYear)
