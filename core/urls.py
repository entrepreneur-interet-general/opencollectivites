from django.urls import path, re_path
from . import views

app_name = "core"
urlpatterns = [
    path(
        "commune/<slug:slug>/",
        views.page_commune_detail,
        name="page_commune_detail",
    ),
    path(
        "epci/<slug:slug>/",
        views.page_epci_detail,
        name="page_epci_detail",
    ),
    path(
        "departement/<slug:slug>/",
        views.page_departement_detail,
        name="page_departement_detail",
    ),
    path(
        "departement/<slug:slug>/liste-communes/",
        views.page_departement_liste_communes,
        name="page_departement_liste_communes",
    ),
    path(
        "departement/<slug:slug>/liste-epcis/",
        views.page_departement_liste_epcis,
        name="page_departement_liste_epcis",
    ),
    path(
        "region/<slug:slug>/",
        views.page_region_detail,
        name="page_region_detail",
    ),
    path(
        "region/<slug:slug>/liste-communes/",
        views.page_region_liste_communes,
        name="page_region_liste_communes",
    ),
    path(
        "region/<slug:slug>/liste-epcis/",
        views.page_region_liste_epcis,
        name="page_region_liste_epcis",
    ),
    path(
        "region/<slug:slug>/liste-departements/",
        views.page_region_liste_departements,
        name="page_region_liste_departements",
    ),
    re_path(
        r"^compare\/commune\/(?P<slug1>[-\w]+)\/(?P<slug2>[-\w]+)\/?(?P<slug3>[-\w]+)?\/?(?P<slug4>[-\w]+)?\/?",
        views.page_commune_compare,
        name="page_commune_compare",
    ),
    path(
        "export/commune/<slug:slug>",
        views.csv_commune_export,
        name="csv_commune_export",
    ),
    re_path(
        r"^compare_export\/commune\/(?P<slug1>[-\w]+)\/(?P<slug2>[-\w]+)\/?(?P<slug3>[-\w]+)?\/?(?P<slug4>[-\w]+)?\/?",
        views.csv_compare_communes_from_list,
        name="csv_compare_communes_from_list",
    ),
    path(
        "compare_export/departement/membres/<slug:slug>",
        views.csv_departement_compare_communes,
        name="csv_departement_compare_communes",
    ),
    path(
        "compare_export/epci/membres/<slug:slug>",
        views.csv_epci_compare_communes,
        name="csv_epci_compare_communes",
    ),
    re_path(
        r"^compare\/.*",
        views.page_not_yet,
        name="page_place_compare",
    ),
    path("publications/", views.page_publications, name="page_publications"),
    path("tests/", views.page_tests, name="page_tests"),
    path("plan/", views.page_sitemap, name="page_sitemap"),
    path("test_404/", views.error404, {"exception": Exception()}, name="page_test_404"),
    path("test_500/", views.error500, {"exception": Exception()}, name="page_test_500"),
    path("test_50x/", views.error50x, {"exception": Exception()}, name="page_test_50x"),
]
