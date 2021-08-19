# Generated by Django 3.2.6 on 2021-08-18 12:24

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtailmarkdown.blocks
import wagtailsvg.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('pages', '0002_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('svg', wagtailsvg.blocks.SvgChooserBlock()), ('section_with_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(form_classname='Titre')), ('text', wagtail.core.blocks.RichTextBlock(form_classname='Texte')), ('image_position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Gauche'), ('right', 'Droite')], classname='Position de l’image')), ('image', wagtailsvg.blocks.SvgChooserBlock(form_classname='Image'))])), ('markdown', wagtailmarkdown.blocks.MarkdownBlock())], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='richtextpage',
            name='page_ptr',
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock()), ('svg', wagtailsvg.blocks.SvgChooserBlock()), ('section_with_image', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(form_classname='Titre')), ('text', wagtail.core.blocks.RichTextBlock(form_classname='Texte')), ('image_position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Gauche'), ('right', 'Droite')], classname='Position de l’image')), ('image', wagtailsvg.blocks.SvgChooserBlock(form_classname='Image'))]))], blank=True),
        ),
        migrations.DeleteModel(
            name='MarkdownPage',
        ),
        migrations.DeleteModel(
            name='RichTextPage',
        ),
    ]
