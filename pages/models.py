from wagtail.core.blocks.list_block import ListBlock
from core.services.publications import documents_to_cards, list_documents
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks.field_block import RichTextBlock, CharBlock, ChoiceBlock
from wagtail.core.models import Page
from wagtail.core.blocks import StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock
from wagtailsvg.blocks import SvgChooserBlock

from pages.services.wagtail_dsfr import blocks as dsfr_blocks


class SectionWithImageBlock(StructBlock):
    title = CharBlock(heading="Titre")
    text = RichTextBlock(heading="Texte")
    image_position = ChoiceBlock(
        choices=[("left", "Gauche"), ("right", "Droite")],
        heading="Position de l’image",
    )
    image = SvgChooserBlock(heading="Image")

    class Meta:
        icon = "doc-full"
        label = "Paragraphe avec image"
        template = "pages/blocks/section_with_image.html"


class HomePage(Page):
    body = StreamField(
        [
            ("text", RichTextBlock(label="Paragraphe")),
            ("svg", SvgChooserBlock()),
            ("section_with_image", SectionWithImageBlock()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body", heading="Contenu"),
    ]

    subpage_types = ["pages.ContentPage"]

    def get_homepage_tiles(self):
        tools = list_documents(publication_page=5, limit=4)
        return documents_to_cards(tools)

    def get_context(self, request):
        context = super().get_context(request)

        context["skiplinks"] = [
            {"link": "#content", "label": "Contenu"},
            {"link": "#oc-home-search", "label": "Recherche"},
        ]
        return context


class ContentPage(Page):
    body = StreamField(
        [
            ("section", RichTextBlock(label="Paragraphe")),
            ("section_with_image", SectionWithImageBlock()),
            ("image", ImageChooserBlock()),
            ("svg", SvgChooserBlock()),
            ("markdown", MarkdownBlock()),
            ("alert", dsfr_blocks.AlertBlock()),
            (
                "accordion_group",
                ListBlock(
                    dsfr_blocks.AccordionBlock(), icon="list-ul", label="Accordéons"
                ),
            ),
            ("callout", dsfr_blocks.CalloutBlock()),
            ("highlight", dsfr_blocks.HighlightBlock()),
            ("link", dsfr_blocks.LinkBlock()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body", heading="Contenu"),
    ]

    parent_page_types = ["pages.HomePage", "pages.ContentPage"]
    subpage_types = ["pages.ContentPage"]

    def get_context(self, request):
        context = super().get_context(request)

        context["skiplinks"] = [
            {"link": "#content", "label": "Contenu"},
        ]
        return context
