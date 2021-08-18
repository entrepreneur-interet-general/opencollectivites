# Generated by Django 3.2.6 on 2021-08-18 13:22

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmarkdown.blocks
import wagtailsvg.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_alter_contentpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.RichTextBlock(heading='Paragraphe')), ('section_with_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(heading='Titre')), ('text', wagtail.core.blocks.RichTextBlock(heading='Texte')), ('image_position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Gauche'), ('right', 'Droite')], heading='Position de l’image')), ('image', wagtailsvg.blocks.SvgChooserBlock(heading='Image'))])), ('image', wagtail.images.blocks.ImageChooserBlock()), ('svg', wagtailsvg.blocks.SvgChooserBlock()), ('markdown', wagtailmarkdown.blocks.MarkdownBlock())], blank=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('svg', wagtailsvg.blocks.SvgChooserBlock()), ('section_with_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(heading='Titre')), ('text', wagtail.core.blocks.RichTextBlock(heading='Texte')), ('image_position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Gauche'), ('right', 'Droite')], heading='Position de l’image')), ('image', wagtailsvg.blocks.SvgChooserBlock(heading='Image'))]))], blank=True),
        ),
    ]
