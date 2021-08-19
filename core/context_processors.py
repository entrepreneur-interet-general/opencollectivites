from django.urls.base import reverse
from django.http import HttpRequest
from core.models import Topic


def topics_processor(request: HttpRequest) -> dict:
    raw_topics = Topic.objects.all()
    page_publications = reverse("core:page_publications")
    topics = []

    for topic in raw_topics:
        topics.append(
            {
                "title": topic.name,
                "url": f"{page_publications}?topic={topic.id}",
                "image_path": f"/static{topic.icon_path}",
                "svg_icon": True,
            }
        )
    return {"context_topics": topics}
