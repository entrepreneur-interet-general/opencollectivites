from django.contrib import admin
from francedata.services.django_admin import TimeStampModelAdmin
from collectivity_pages import models


class DataRowInline(admin.TabularInline):
    search_fields = ("label", "key")
    ordering = ["rank"]
    model = models.DataRow
    extra = 0


@admin.register(models.DataTable)
class DataTableAdmin(TimeStampModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "page_type", "rows_count")
    list_filter = ("page_type",)
    prepopulated_fields = {
        "slug": (
            "page_type",
            "name",
        )
    }
    ordering = ["page_type"]
    inlines = [DataRowInline]

    def rows_count(self, obj):
        count = getattr(obj, "datarow_set").count()
        return count

    rows_count.short_description = "Lignes"


@admin.register(models.CollectivityMessage)
class CollectivityMessageAdmin(TimeStampModelAdmin):
    list_display = (
        "id",
        "collectivity_type",
        "coll_name",
        "message",
    )
    list_filter = ("collectivity_type",)

    @admin.display(description="Collectivité")
    def coll_name(self, obj):
        return obj.get_coll_name()


@admin.register(models.Vintage)
class VintageAdmin(TimeStampModelAdmin):
    list_display = ("key", "value")
    ordering = ["key"]
