from django.test import SimpleTestCase
from django.template import Context, Template


class CreateDsfrCssTagTest(SimpleTestCase):
    def test_css_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %}" "{% dsfr_css %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            '<link rel="stylesheet" href="/static/dsfr/dist/css/dsfr.min.css">',
            rendered_template,
        )


class CreateDsfrJsTagTest(SimpleTestCase):
    def test_js_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %}" "{% dsfr_js %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
<script type="module" src="/static/dsfr/dist/js/dsfr.module.min.js"></script>
<script type="text/javascript" nomodule src="/static/dsfr/dist/js/dsfr.nomodule.min.js"></script>""",
            rendered_template,
        )


class CreateDsfrFaviconTagTest(SimpleTestCase):
    def test_favicon_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %}" "{% dsfr_favicon %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
<link rel="apple-touch-icon" href="/static/dsfr/dist/favicons/apple-touch-icon.png"><!-- 180×180 -->
<link rel="icon" href="/static/dsfr/dist/favicons/favicon.svg" type="image/svg+xml">
<link rel="shortcut icon" href="/static/dsfr/dist/favicons/favicon.ico" type="image/x-icon">
<!-- 32×32 -->
<link rel="manifest" href="/static/dsfr/dist/favicons/manifest.webmanifest"
crossorigin="use-credentials">""",
            rendered_template,
        )


class CreateDsfrBreadcrumbTagTest(SimpleTestCase):
    breadcrumb_data = {
        "links": [{"url": "test-url", "title": "Test title"}],
        "current": "Test page",
    }

    context = Context({"breadcrumb_data": breadcrumb_data})
    template_to_render = Template(
        "{% load dsfr_tags %}" "{% dsfr_breadcrumb breadcrumb_data %}"
    )

    def test_breadcrumb_tag_current_page(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<a class="fr-breadcrumb__link" aria-current="page">Test page</a>""",
            rendered_template,
        )

    def test_breadcrumb_tag_middle_link(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<a class="fr-breadcrumb__link" href="test-url">Test title</a>""",
            rendered_template,
        )
