from django.urls.base import reverse
from django.http import HttpRequest
from core.models import Topic


def topics_processor(request: HttpRequest) -> dict:
    raw_topics = Topic.objects.all()
    page_publications = reverse("core:page_publications")
    topics = []

    for topic in raw_topics:
        if "media" in topic.icon_path:
            icon_path = f"/media/{topic.icon_path}"
        else:
            icon_path = f"/static{topic.icon_path}"
        topics.append(
            {
                "title": topic.name,
                "url": f"{page_publications}?topic={topic.id}",
                "image_path": icon_path,
            }
        )
    return {"context_topics": topics}
