# Generated by Django 3.2.7 on 2021-09-23 15:48

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmarkdown.blocks
import wagtailsvg.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20210818_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.RichTextBlock(label='Paragraphe')), ('section_with_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(heading='Titre')), ('text', wagtail.core.blocks.RichTextBlock(heading='Texte')), ('image_position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Gauche'), ('right', 'Droite')], heading='Position de l’image')), ('image', wagtailsvg.blocks.SvgChooserBlock(heading='Image'))])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('svg', wagtailsvg.blocks.SvgChooserBlock()), ('markdown', wagtailmarkdown.blocks.MarkdownBlock()), ('alert', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Titre')), ('content', wagtail.core.blocks.RichTextBlock(label='Contenu', required=False)), ('type', wagtail.core.blocks.ChoiceBlock(choices=[('error', 'Erreur'), ('success', 'Succès'), ('info', 'Information')]))])), ('accordion_group', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Titre')), ('content', wagtail.core.blocks.RichTextBlock(label='Contenu'))]), icon='list-ul', label='Accordéons')), ('callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Titre', required=False)), ('content', wagtail.core.blocks.RichTextBlock(label='Contenu')), ('icon', wagtail.core.blocks.CharBlock(help_text="Une classe d'icône du design système, par exemple fr-fi-alert-line. <a href='https://gouvfr.atlassian.net/wiki/spaces/DB/pages/222331396/Ic+nes+-+Icons'>Voir la liste complète</a>", label='Icône', required=False)), ('button', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(required=False)), ('label', wagtail.core.blocks.CharBlock(required=False))], label='Bouton', required=False))])), ('highlight', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.RichTextBlock(label='Contenu'))])), ('link', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(label='Lien')), ('label', wagtail.core.blocks.CharBlock(label='Libellé')), ('icon', wagtail.core.blocks.ChoiceBlock(choices=[('fr-fi-arrow-right-line', 'Lien interne'), ('fr-fi-external-link-line', 'Lien externe'), ('fr-fi-download-line', 'Téléchargement')], help_text="Une classe d'icône du design système, par exemple fr-fi-alert-line", label='Icône'))]))], blank=True),
        ),
    ]
