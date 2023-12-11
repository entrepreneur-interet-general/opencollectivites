from django.db.models.query import QuerySet
from collectivity_pages.models import CollectivityMessage
from core.services.utils import format_number


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


def format_raw_data(raw_data: str, format_for_web: bool) -> str:
    """
    Formats a data_point according to its type
    """
    # Managing empty strings, then casting according to the proper datatype
    if raw_data.value == "":
        formatted_value = raw_data.value
    elif raw_data.datatype == "int":
        formatted_value = format_number(int(float(raw_data.value)), format_for_web)
    elif raw_data.datatype == "float":
        formatted_value = format_number(float(raw_data.value), format_for_web)
    elif raw_data.datatype == "bool":
        formatted_value = format_boolean(raw_data.value)
    else:
        formatted_value = raw_data.value

    return formatted_value


def get_messages_for_collectivity(
    collectivity_type: str, collectivity_slug: str
) -> QuerySet:
    return CollectivityMessage.objects.filter(
        collectivity_type=collectivity_type, collectivity_slug=collectivity_slug
    )
