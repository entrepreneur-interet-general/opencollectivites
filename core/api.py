from ninja import Router
from typing import List

from core.models import Scope, Topic, Document
from core.schemas import ScopeSchema, TopicSchema, FilterSchema, DocumentSchema

router = Router()


@router.get("/scopes", response=List[ScopeSchema], tags=["core"])
def list_scopes(request):
    qs = Scope.objects.all()
    return qs


@router.get("/scopes/{scope_id}", response=ScopeSchema, tags=["core"])
def get_scope(request, topic_id: int):
    item = get_object_or_404(Scope, id=scope_id)
    return item


@router.get("/topics", response=List[TopicSchema], tags=["core"])
def list_topics(request):
    qs = Topic.objects.all()
    return qs


@router.get("/topics/{topic_id}", response=TopicSchema, tags=["core"])
def get_topic(request, topic_id: int):
    item = get_object_or_404(Topic, id=topic_id)
    return item


@router.get("/filters", response=FilterSchema, tags=["core"])
def list_filters(request):
    """Returns all the filters in a single query"""
    scopes = list(Scope.objects.all())
    topics = list(Topic.objects.all())

    qs = {"scopes": scopes, "topics": topics}
    return qs


@router.get("/documents", response=List[DocumentSchema], tags=["core"])
def list_documents(request, topic: int = None, scope: int = None, page: int = None):
    """
    Lists all **published** documents.
    """
    qs = Document.objects.filter(is_published=True)
    if topic:
        qs = qs.filter(topics__id=topic)
    if scope:
        qs = qs.filter(scope__id=scope)
    if page:
        qs = qs.filter(publication_pages__id=page)
    return qs


@router.get("/documents/{document_id}", response=DocumentSchema, tags=["core"])
def get_document(request, document_id: int):
    """
    Get a **published** document.
    """
    item = get_object_or_404(Document, id=document_id, is_published=True)
    return item
