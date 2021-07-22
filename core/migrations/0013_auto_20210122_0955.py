# Generated by Django 3.1.5 on 2021-01-22 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("feeds", "0009_auto_20201104_1023"),
        ("core", "0012_metadata"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="datayear",
            options={"ordering": ["year"], "verbose_name": "millésime"},
        ),
        migrations.AlterModelOptions(
            name="documenttype",
            options={
                "ordering": ["name"],
                "verbose_name": "type de document",
                "verbose_name_plural": "types de document",
            },
        ),
        migrations.AlterModelOptions(
            name="editor",
            options={"ordering": ["name"], "verbose_name": "éditeur"},
        ),
        migrations.AlterModelOptions(
            name="metadata",
            options={"verbose_name": "métadonnée"},
        ),
        migrations.AlterModelOptions(
            name="pagetype",
            options={
                "ordering": ["name"],
                "verbose_name": "type de page",
                "verbose_name_plural": "types de page",
            },
        ),
        migrations.AlterModelOptions(
            name="scope",
            options={"ordering": ["name"], "verbose_name": "portée"},
        ),
        migrations.AlterModelOptions(
            name="topic",
            options={"ordering": ["name"], "verbose_name": "sujet"},
        ),
        migrations.AddField(
            model_name="document",
            name="regions",
            field=models.ManyToManyField(to="francesubdivisions.Region"),
        ),
        migrations.AlterField(
            model_name="datayear",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="datayear",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="datayear",
            name="year",
            field=models.PositiveSmallIntegerField(verbose_name="année"),
        ),
        migrations.AlterField(
            model_name="document",
            name="base_domain",
            field=models.CharField(max_length=100, null=True, verbose_name="domaine"),
        ),
        migrations.AlterField(
            model_name="document",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="is_published",
            field=models.BooleanField(null=True, verbose_name="est publié"),
        ),
        migrations.AlterField(
            model_name="document",
            name="last_update",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="document",
            name="publication_pages",
            field=models.ManyToManyField(
                to="core.PageType", verbose_name="pages de publication"
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="rss_post",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="feeds.post",
                verbose_name="Post associé",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="scope",
            field=models.ManyToManyField(to="core.Scope", verbose_name="portée"),
        ),
        migrations.AlterField(
            model_name="document",
            name="title",
            field=models.CharField(max_length=100, verbose_name="titre"),
        ),
        migrations.AlterField(
            model_name="document",
            name="topics",
            field=models.ManyToManyField(to="core.Topic", verbose_name="sujet"),
        ),
        migrations.AlterField(
            model_name="document",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="url",
            field=models.URLField(null=True, verbose_name="URL"),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="icon_url",
            field=models.URLField(null=True, verbose_name="URL de l’icône"),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="name",
            field=models.CharField(max_length=100, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="documenttype",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="editor",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="editor",
            name="name",
            field=models.CharField(max_length=100, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="editor",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="metadata",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="metadata",
            name="prop",
            field=models.CharField(max_length=100, verbose_name="propriété"),
        ),
        migrations.AlterField(
            model_name="metadata",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="metadata",
            name="value",
            field=models.CharField(max_length=255, verbose_name="valeur"),
        ),
        migrations.AlterField(
            model_name="pagetype",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="pagetype",
            name="name",
            field=models.CharField(max_length=100, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="pagetype",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="scope",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="scope",
            name="name",
            field=models.CharField(max_length=100, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="scope",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="base_domain",
            field=models.CharField(max_length=100, null=True, verbose_name="Domaine"),
        ),
        migrations.AlterField(
            model_name="source",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="editor",
            field=models.ManyToManyField(to="core.Editor", verbose_name="éditeur"),
        ),
        migrations.AlterField(
            model_name="source",
            name="rssfeed",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="feeds.source",
                verbose_name="flux RSS",
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="title",
            field=models.CharField(max_length=100, verbose_name="titre"),
        ),
        migrations.AlterField(
            model_name="source",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="url",
            field=models.URLField(null=True, verbose_name="URL"),
        ),
        migrations.AlterField(
            model_name="topic",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="date de création"
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="icon_url",
            field=models.URLField(null=True, verbose_name="URL de l’icône"),
        ),
        migrations.AlterField(
            model_name="topic",
            name="name",
            field=models.CharField(max_length=100, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="topic",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="date de modification"
            ),
        ),
    ]
