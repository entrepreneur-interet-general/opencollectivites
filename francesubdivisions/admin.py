from django.contrib import admin

from francesubdivisions import models

admin.site.register(models.Region)
admin.site.register(models.Departement)
admin.site.register(models.EpciType)
admin.site.register(models.Epci)
admin.site.register(models.Commune)
