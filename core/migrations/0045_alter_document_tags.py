# Generated by Django 3.2.7 on 2021-10-07 16:32

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('core', '0044_document_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='documents_tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
