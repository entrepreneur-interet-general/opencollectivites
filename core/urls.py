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
        views.page_not_yet,
        name="page_epci_detail",
    ),
    re_path(
        r"^compare\/commune\/(?P<siren1>\d{9})\/(?P<siren2>\d{9})\/?(?P<siren3>\d{9})?\/?(?P<siren4>\d{9})?\/?",
        views.page_commune_compare,
        name="page_commune_compare",
    ),
    path("tests", views.page_tests, name="page_tests"),
    path("", views.page_index, name="page_index"),
]
