from wagtail.core import blocks


class AccordionBlock(blocks.StructBlock):
    """
    To be used inside a ListBlock.

    On the model:
    body = StreamField(
        [
            [...],
            (
                "accordion_group",
                blocks.ListBlock(
                    dsfr_blocks.AccordionBlock(), icon="list-ul", label="Accordéons"
                ),
            ),
        ],
    )

    On the template:
    {% for block in page.body %}
        {% if block.block_type == 'accordion_group' %}
            <ul class="fr-accordions-group">
                {% for accordion in block.value %}
                    {% with "accordion"|hyphenate:forloop.parentloop.counter|hyphenate:forloop.counter as accordion_id %}
                        <li>{% include_block accordion with block_id=accordion_id %}</li>
                    {% endwith %}
                {% endfor %}
            </ul>
        {% else %}
            [...]
        {% endif %}
    {% endfor %}
    """

    title = blocks.CharBlock(label="Titre")
    content = blocks.RichTextBlock(label="Contenu")

    class Meta:
        icon = "list-ul"
        label = "Accordéon"
        template = "pages/dsfr_blocks/accordion.html"


class AlertBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    content = blocks.RichTextBlock(label="Contenu", required=False)
    type = blocks.ChoiceBlock(
        choices=[("error", "Erreur"), ("success", "Succès"), ("info", "Information")]
    )

    class Meta:
        icon = "help"
        label = "Alerte"
        template = "pages/dsfr_blocks/alert.html"


class CalloutBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre", required=False)
    content = blocks.RichTextBlock(label="Contenu")

    icon = blocks.CharBlock(
        label="Icône",
        required=False,
        help_text="Une classe d'icône du design système, par exemple fr-fi-alert-line. <a href='https://gouvfr.atlassian.net/wiki/spaces/DB/pages/222331396/Ic+nes+-+Icons'>Voir la liste complète</a>",
    )
    button = blocks.StructBlock(
        [
            ("url", blocks.URLBlock(required=False)),
            ("label", blocks.CharBlock(required=False)),
        ],
        label="Bouton",
        required=False,
    )

    class Meta:
        icon = "doc-full-inverse"
        label = "Mise en avant"
        template = "pages/dsfr_blocks/callout.html"


class HighlightBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(label="Contenu")

    class Meta:
        icon = "doc-full-inverse"
        label = "Mise en exergue"
        template = "pages/dsfr_blocks/highlight.html"


class LinkBlock(blocks.StructBlock):
    url = blocks.URLBlock(label="Lien")
    label = blocks.CharBlock(label="Libellé")

    icon = blocks.ChoiceBlock(
        label="Icône",
        help_text="Une classe d'icône du design système, par exemple fr-fi-alert-line",
        choices=[
            ("fr-fi-arrow-right-line", "Lien interne"),
            ("fr-fi-external-link-line", "Lien externe"),
            ("fr-fi-download-line", "Téléchargement"),
        ],
        default="fr-fi-arrow-right-line",
    )

    class Meta:
        icon = "link"
        label = "Lien"
        template = "pages/dsfr_blocks/link.html"
