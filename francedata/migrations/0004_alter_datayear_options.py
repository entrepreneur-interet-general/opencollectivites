# Generated by Django 3.2.9 on 2021-12-13 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('francedata', '0003_datamapping_datasourcefile_historicaldatamapping_squashed_0007_alter_datamapping_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datayear',
            options={'get_latest_by': 'year', 'verbose_name': 'millésime'},
        ),
    ]
