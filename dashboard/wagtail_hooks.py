from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape, format_html

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler


@hooks.register("register_admin_menu_item")
def register_adminindex_menu_item():
    return MenuItem(
        "Administration",
        reverse("admin:index"),
        icon_name="cog",
        order=10000,
    )


class UserbarDjangoAdminLinkItem:
    def render(self, request):
        return (
            '<li class="wagtail-userbar__item"><a href="'
            + reverse("admin:index")
            + '" '
            + 'target="_parent" role="menuitem" class="wagtail-userbar-link">'
            + '<svg class="icon icon-cog wagtail-action-icon" aria-hidden="true" focusable="false"><use href="#icon-cog"></use></svg>'
            + "Aller sur l’administration de Django</a></li>"
        )


@hooks.register("construct_wagtail_userbar")
def add_django_admin_link_item(request, items):
    return items.insert(0, UserbarDjangoAdminLinkItem())


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("dashboard/wagtail_theme.css")
    )


class NewWindowExternalLinkHandler(LinkHandler):
    # Source: https://erev0s.com/blog/wagtail-list-tips-and-tricks/#external-site-links-to-open-in-a-new-window
    # This specifies to do this override for external links only.
    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        # Let's add the target attr, and also rel="noopener" + noreferrer fallback.
        # See https://github.com/whatwg/html/issues/4078.
        return f'<a href="{escape(href)}" target="_blank" rel="noopener noreferrer">'


@hooks.register("register_rich_text_features")
def register_external_link(features):
    features.register_link_type(NewWindowExternalLinkHandler)
