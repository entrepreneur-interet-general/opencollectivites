from django.contrib import admin
from francedata.services.django_admin import TimeStampModelAdmin

from bnsp import models

# Register your models here.


@admin.register(models.Query)
class QueryAdmin(TimeStampModelAdmin):
    pass
