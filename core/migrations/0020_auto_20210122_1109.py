# Generated by Django 3.1.5 on 2021-01-22 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20210122_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='logo',
            field=models.ImageField(blank=True, upload_to='logos'),
        ),
    ]
