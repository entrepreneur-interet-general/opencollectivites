from django.shortcuts import render
from django.views.decorators.http import require_safe
from core.models import Scope, Source, Topic
from core.services.utils import init_payload
from francedata.models import Region


@require_safe
def error404(request, exception):
    payload = init_payload("Erreur")
    payload["exception"] = exception
    return render(request, "core/404.html", payload, status=404)


@require_safe
def error500(request, *args, **argv):
    payload = init_payload("Erreur serveur")
    return render(request, "core/500.html", payload, status=500)


@require_safe
def error50x(request, *args, **argv):
    payload = init_payload("Erreur serveur")
    return render(request, "core/50x.html", payload, status=503)


@require_safe
def page_not_yet(request, **kwargs):
    payload = init_payload("Page en construction")
    return render(request, "core/page_not_yet.html", payload)


@require_safe
def page_sitemap(request):
    payload = init_payload("Plan du site")

    regions = Region.objects.order_by("name")
    regions_data = []
    for r in regions:
        regions_data.append(
            {"name": r.name, "slug": r.slug, "counts": r.subdivisions_count()}
        )

    filter_data = {}
    filter_data["topic"] = Topic.objects.order_by("name")
    filter_data["scope"] = Scope.objects.order_by("name")
    filter_data["source"] = Source.objects.order_by("title")
    payload["filter_data"] = filter_data

    payload["regions_data"] = regions_data

    return render(request, "core/sitemap.html", payload)


@require_safe
def page_tests(request):
    payload = init_payload("Tests")
    payload["breadcrumb_with_link"] = {
        "links": [{"url": "test-url", "title": "Test title"}],
        "current": "Test page",
    }
    payload["context"]["hide_brand"] = True
    return render(request, "core/tests.html", payload)
