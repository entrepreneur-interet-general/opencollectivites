from core.services.publications import documents_to_cards, list_documents
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks.field_block import RichTextBlock, CharBlock, ChoiceBlock
from wagtail.core.models import Page
from wagtail.core.blocks import StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock
from wagtailsvg.blocks import SvgChooserBlock


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

    def get_homepage_tiles(self):
        tools = list_documents(publication_page=5, limit=4)
        return documents_to_cards(tools)


class ContentPage(Page):
    body = StreamField(
        [
            ("section", RichTextBlock(label="Paragraphe")),
            ("section_with_image", SectionWithImageBlock()),
            ("image", ImageChooserBlock()),
            ("svg", SvgChooserBlock()),
            ("markdown", MarkdownBlock()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body", heading="Contenu"),
    ]
