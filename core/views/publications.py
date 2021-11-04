from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_GET, require_safe

from core.services.utils import init_payload
from core.services.publications import (
    list_documents,
    documents_to_cards,
    publication_filters,
)


@require_safe
def page_publications(request):
    payload = init_payload("Études, statistiques et outils locaux")

    documents, total_count = list_documents(
        topic=request.GET.get("topic"),
        scope=request.GET.get("scope"),
        document_type=request.GET.get("document_type"),
        publication_page=request.GET.get("publication_page"),
        source_org=request.GET.get("source_org"),
        year=request.GET.get("year"),
        commune=request.GET.get("commune"),
        epci=request.GET.get("epci"),
        departement=request.GET.get("departement"),
        region=request.GET.get("region"),
        before=request.GET.get("before"),
        after=request.GET.get("after"),
    )

    cards = documents_to_cards(documents)

    paginated_docs = Paginator(cards, settings.PUBLICATIONS_PER_PAGE)

    data = {}
    data["total"] = paginated_docs.count
    data["cards_page"] = paginated_docs.get_page(request.GET.get("page"))

    payload["data"] = data

    payload["filters"] = publication_filters(request)

    return render(request, "core/publications.html", payload)
