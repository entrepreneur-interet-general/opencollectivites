from django.contrib import admin

from core import models

admin.site.register(models.Topic)
admin.site.register(models.Scope)
admin.site.register(models.Editor)
admin.site.register(models.Platform)
