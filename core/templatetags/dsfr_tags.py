from django import template
from urllib.parse import urlencode

register = template.Library()
"""
Tags used in the "DSFR" templates.
"""


@register.simple_tag(takes_context=True)
def url_remplace_params(context, **kwargs):
    """
    Allows to make a link that adds or updates a GET parameter while
    keeping the existing ones.
    Useful for combining filters and pagination.

    Sample use:
    <a href="?{% url_remplace_params page=page_obj.next_page_number %}">Next</a>
    """
    query = context["request"].GET.copy()

    for k in kwargs:
        query[k] = kwargs[k]

    return query.urlencode()
