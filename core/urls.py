from django.urls import path, re_path
from . import views

app_name = "core"
urlpatterns = [
    path(
        "commune/<int:siren>/<str:commune_name>",
        views.page_commune_detail,
        name="page_commune_detail",
    ),
    path(
        "epci/<int:siren>/<str:epci_name>",
        views.page_epci_detail,
        name="page_epci_detail",
    ),
    path(
        "<str:place_type>/<int:siren>/<str:epci_name>",
        views.page_not_yet,
        name="page_place_detail",
    ),
    re_path(
        r"^compare\/commune\/(?P<siren1>\d{9})\/(?P<siren2>\d{9})\/?(?P<siren3>\d{9})?\/?(?P<siren4>\d{9})?\/?",
        views.page_commune_compare,
        name="page_commune_compare",
    ),
    re_path(
        r"^compare\/.*",
        views.page_not_yet,
        name="page_place_compare",
    ),
    path(
        "region/liste_departements/<slug:slug>",
        views.page_not_yet,
        name="page_region_departements",
    ),
    path(
        "region/liste_communes/<slug:slug>",
        views.page_not_yet,
        name="page_region_communes",
    ),
    path("publications", views.page_publications, name="page_publications"),
    path("tests", views.page_tests, name="page_tests"),
    path("mentions-legales", views.page_legal, name="page_legal"),
    path("plan", views.page_sitemap, name="page_sitemap"),
    path("test_404", views.error404, {"exception": Exception()}, name="page_test_404"),
    path("", views.page_index, name="page_index"),
]
