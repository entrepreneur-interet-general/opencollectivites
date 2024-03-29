# Generated by Django 3.2.7 on 2021-10-07 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("external_apis", "0002_alter_opendatasoftquery_query"),
        ("external_apis", "0001_squashed_0006_auto_20211007_1433"),
        ("core", "0042_document_bnsp_query"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="ods_queries",
            field=models.ManyToManyField(
                blank=True,
                to="external_apis.OpenDataSoftQuery",
                verbose_name="Requête OpenDataSoft associée",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="body",
            field=models.TextField(blank=True, verbose_name="corps"),
        ),
    ]
