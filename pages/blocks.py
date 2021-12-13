from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.core import blocks
from wagtail.core.blocks.field_block import RichTextBlock, CharBlock, ChoiceBlock

from wagtailsvg.blocks import SvgChooserBlock

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name


class SectionWithImageBlock(blocks.StructBlock):
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


LIMITED_RICHTEXTFIELD_FEATURES = getattr(
    settings, "LIMITED_RICHTEXTFIELD_FEATURES", None
)

LANGUAGE_CHOICES = [
    ("bash", "bash"),
    ("css", "css"),
    ("html", "html"),
    ("javascript", "javascript"),
    ("json", "json"),
    ("markdown", "markdown"),
    ("python", "python"),
    ("sql", "sql"),
    ("toml", "toml"),
    ("xml", "xml"),
]


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES, default="bash")
    text = blocks.TextBlock()

    class Meta:
        template = "blog/blocks/code_block.html"
        icon = "code"
        label = "Bloc de code"

    def render(self, value, **kwargs):
        src = value["text"].strip("\n")
        lang = value["language"]
        lexer = get_lexer_by_name(lang)
        css_classes = ["code", "dsfr-code"]

        formatter = get_formatter_by_name(
            "html",
            linenos=False,
            cssclass=" ".join(css_classes),
            noclasses=False,
            wrapcode=True,
        )
        return mark_safe(highlight(src, lexer, formatter))
