# Generated by Django 3.2.8 on 2021-10-11 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_apis', '0004_bnspquery'),
        ('core', '0046_auto_20211011_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='bnsp_queries',
            field=models.ManyToManyField(blank=True, to='external_apis.BnspQuery', verbose_name='Requête BNSP associée'),
        ),
        migrations.AlterField(
            model_name='document',
            name='ods_queries',
            field=models.ManyToManyField(blank=True, to='external_apis.OpenDataSoftQuery', verbose_name='Requêtes OpenDataSoft associées'),
        ),
    ]
