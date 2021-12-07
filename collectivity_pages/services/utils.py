from django.db.models.query import QuerySet
from collectivity_pages.models import CollectivityMessage


def format_civility(civility: str):
    """
    Format the civility and returns it as html, so it has to be invoked with |safe in a Django template.
    """
    if civility == "Mme":
        return "M<sup>me</sup>"
    elif civility == "M":
        return "M."
    else:
        return ""


def format_boolean(boolean_str: str) -> str:
    return "Oui" if int(boolean_str) else "Non"


def get_messages_for_collectivity(
    collectivity_type: str, collectivity_slug: str
) -> QuerySet:
    return CollectivityMessage.objects.filter(
        collectivity_type=collectivity_type, collectivity_slug=collectivity_slug
    )
