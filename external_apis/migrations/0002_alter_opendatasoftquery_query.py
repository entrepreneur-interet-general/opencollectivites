# Generated by Django 3.2.7 on 2021-10-07 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_apis', '0001_squashed_0006_auto_20211007_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opendatasoftquery',
            name='query',
            field=models.CharField(help_text="Entrer '*' pour rechercher toutes les entrées", max_length=1000, verbose_name='requête'),
        ),
    ]