from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from francedata.services.django_admin import TimeStampModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from external_apis.models import DataMapping, OpenDataSoftEndpoint, OpenDataSoftQuery


class DataMappingAdmin(SimpleHistoryAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


class OpenDataSoftEndpointAdmin(TimeStampModelAdmin):
    pass


class OpenDataSoftQueryAdmin(TimeStampModelAdmin):
    pass


admin.site.register(DataMapping, DataMappingAdmin)
admin.site.register(OpenDataSoftEndpoint, OpenDataSoftEndpointAdmin)
admin.site.register(OpenDataSoftQuery, OpenDataSoftQueryAdmin)
