from django import template
import toml

register = template.Library()


@register.simple_tag
def version_number():
    return toml.load("pyproject.toml")["tool"]["poetry"]["version"]
