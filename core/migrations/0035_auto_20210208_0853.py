# Generated by Django 3.1.6 on 2021-02-08 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20210122_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='icon_url',
        ),
        migrations.AddField(
            model_name='topic',
            name='icon_path',
            field=models.CharField(max_length=255, null=True, verbose_name='Chemin de l’icône'),
        ),
    ]
