# Generated by Django 3.2.8 on 2021-10-12 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20211011_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='bnsp_query',
        ),
    ]
