from core.models import Document
from pprint import pprint
from core.api import list_documents


def list_documents(
    topic: int = None,
    scope: int = None,
    document_type: int = None,
    publication_page: int = None,
    limit: int = None,
    offset: int = 0,
):
    """
    Lists all **published** documents.
    """
    qs = Document.objects.filter(is_published=True)

    # Filters
    if topic:
        qs = qs.filter(topics__id=topic)
    if scope:
        qs = qs.filter(scope__id=scope)
    if document_type:
        qs = qs.filter(document_type__id=document_type)
    if publication_page:
        qs = qs.filter(publication_pages__id=publication_page)

    # Pagination
    if not limit or limit > 20:
        limit = 20

    total = qs.count()
    if limit:
        qs = qs[offset : offset + limit]

    response = {"documents": list(qs), "total": total}

    pprint(response)
    return response