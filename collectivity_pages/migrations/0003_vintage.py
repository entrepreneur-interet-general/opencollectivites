# Generated by Django 3.2.9 on 2021-11-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectivity_pages', '0002_auto_20211130_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vintage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('key', models.CharField(max_length=100, verbose_name='clef')),
                ('value', models.CharField(max_length=100, verbose_name='valeur')),
            ],
            options={
                'verbose_name': 'millésime',
            },
        ),
    ]
