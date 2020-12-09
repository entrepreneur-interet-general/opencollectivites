from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from aspic.views import CommuneBaseViewSet, FicheCommuneView
from rest_framework import renderers

commune_base_list = CommuneBaseViewSet.as_view(
    {
        "get": "list",
    }
)
commune_base_detail = CommuneBaseViewSet.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns = format_suffix_patterns(
    [
        path("commune/base/", commune_base_list, name="commune-base-list"),
        path(
            "commune/base/<int:siren>/",
            commune_base_detail,
            name="commnune-base-detail",
        ),
        path("fiche-commune/<int:siren>/", FicheCommuneView, name="fiche-commune"),
    ]
)
