from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from francesubdivisions import views

urlpatterns = [
    path("regions/", views.RegionList.as_view(), name="region-list"),
    path("regions/<int:pk>/", views.RegionDetail.as_view(), name="region-detail"),
    path("departements/", views.DepartementList.as_view(), name="departement-list"),
    path(
        "departements/<int:pk>/",
        views.DepartementDetail.as_view(),
        name="departement-detail",
    ),
    path("epci/", views.EpciList.as_view(), name="epci-list"),
    path("epci/<int:pk>/", views.EpciDetail.as_view(), name="epci-detail"),
    path("communes/", views.CommuneList.as_view(), name="commune-list"),
    path("communes/<int:pk>/", views.CommuneDetail.as_view(), name="commune-detail"),
    path("", views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)