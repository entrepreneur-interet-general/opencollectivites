from django.contrib import admin

from francesubdivisions import models


class CommuneAdmin(admin.ModelAdmin):
    search_fields = ("name", "insee", "siren")


admin.site.register(models.Region)
admin.site.register(models.Departement)
admin.site.register(models.EpciType)
admin.site.register(models.Epci)
admin.site.register(models.Commune, CommuneAdmin)
