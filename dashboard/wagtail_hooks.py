from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks


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
