from core.models import Document
from pprint import pprint
from core.api import list_documents


def list_documents(
    topic: int = None,
    scope: int = None,
    document_type: int = None,
    publication_page: int = None,
):
    """
    Lists **published** documents, with optional filters
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
    return qs


def documents_to_cards(qs):
    """
    Converts a queryset of documents to a list of cards
    """
    cards = []
    for doc in qs:
        if len(doc.document_type.all()):
            detail = f"{doc.document_type.all()[0]} | {doc.last_update}"
        else:
            detail = f"{doc.last_update}"

        if doc.source and len(doc.source.editor.all()):
            detail = (
                f"{detail} • {', '.join([ i.acronym for i in doc.source.editor.all()])}"
            )
        cards.append(
            {
                "detail": detail,
                "link": doc.url,
                "title": doc.title,
                "description": doc.body,
                "image": doc.image_url,
            }
        )

    return cards