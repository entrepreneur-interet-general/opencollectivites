from ninja import Router
from typing import List

from core.models import Topic, Document
from core.schemas import TopicSchema, DocumentSchema

router = Router()


@router.get("/topics", response=List[TopicSchema], tags=["core"])
def list_topics(request):
    qs = Topic.objects.all()
    return qs


@router.get("/topics/{topic_id}", response=TopicSchema, tags=["core"])
def get_topic(request, topic_id: int):
    item = get_object_or_404(Topic, id=topic_id)
    return item


@router.get("/documents", response=List[DocumentSchema], tags=["core"])
def list_documents(request):
    """
    Lists all **published** documents.
    """
    qs = Document.objects.filter(is_published=True)
    print(qs)
    return qs


@router.get("/documents/{document_id}", response=DocumentSchema, tags=["core"])
def get_document(request, document_id: int):
    """
    Get a **published** document.
    """
    item = get_object_or_404(Document, id=document_id, is_published=True)
    return item
