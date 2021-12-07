from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from collectivity_pages.services.communes import (
    compare_communes_for_export,
)

from francedata.models import Departement, Commune, Epci


###############
# CSV exports #
###############
@require_safe
def csv_commune_export(request, slug):
    commune = Commune.objects.filter(slug=slug)
    # Commune.objects.filter is used instead of get_object_or_404 because
    # compare_communes_for_export expects a QuerySet
    filename = f"export-commune-{slug}"
    response = compare_communes_for_export(commune, filename)
    return response


@require_safe
def csv_compare_communes_from_list(request, slug1, slug2, slug3=0, slug4=0):
    slugs = [slug1, slug2]
    if slug3:
        slugs.append(slug3)
    if slug4:
        slugs.append(slug4)

    communes = Commune.objects.filter(slug__in=slugs)
    filename = f"comparaisons-communes-{'-'.join(slugs)}"

    response = compare_communes_for_export(communes, filename)
    return response


@require_safe
def csv_epci_compare_communes(request, slug):
    epci = get_object_or_404(Epci, slug=slug)
    filename = f"comparaisons-communes-{slug}"
    response = compare_communes_for_export(epci.commune_set.all(), filename)
    return response


@require_safe
def csv_departement_compare_communes(request, slug):
    departement = get_object_or_404(Departement, slug=slug)
    filename = f"comparaisons-communes-{slug}"
    response = compare_communes_for_export(departement.commune_set.all(), filename)
    return response
