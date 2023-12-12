# Generated by Django 3.2.5 on 2021-07-22 08:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import francedata.services.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('insee', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^([0-1]\\d{4}|2[AB1-9]\\d{3}|[3-8]\\d{4}|9[0-5]\\d{3}|97[12346]\\d{2})$')], verbose_name='identifiant Insee')),
                ('siren', models.CharField(blank=True, max_length=9, validators=[francedata.services.validators.validate_siren], verbose_name='numéro Siren')),
                ('population', models.IntegerField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'commune',
            },
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('title', models.CharField(max_length=255, verbose_name='titre')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'source',
            },
        ),
        migrations.CreateModel(
            name='DataYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('year', models.PositiveSmallIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'millésime',
            },
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('insee', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^([0-1]\\d|2[AB1-9]|[3-8]\\d|9[0-5]|97[12346])$')], verbose_name='identifiant Insee')),
                ('siren', models.CharField(blank=True, max_length=9, null=True, validators=[francedata.services.validators.validate_siren], verbose_name='numéro Siren')),
                ('category', models.CharField(blank=True, choices=[('DEPT', 'Département'), ('PARIS', 'Paris'), ('ML', 'Métropole de Lyon')], max_length=5, null=True, verbose_name='catégorie')),
                ('slug', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name': 'département',
            },
        ),
        migrations.CreateModel(
            name='Epci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('epci_type', models.CharField(blank=True, choices=[('CA', 'Communauté d’agglomération'), ('CC', 'Communauté de communes'), ('CU', 'Communauté urbaine'), ('MET69', 'Métropole de Lyon'), ('METRO', 'Métropole')], max_length=5, null=True, verbose_name='type d’EPCI')),
                ('siren', models.CharField(max_length=9, validators=[francedata.services.validators.validate_siren], verbose_name='numéro Siren')),
                ('slug', models.CharField(blank=True, default='', max_length=100)),
                ('years', models.ManyToManyField(to='francedata.DataYear', verbose_name='millésimes')),
            ],
            options={
                'verbose_name': 'EPCI',
            },
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('prop', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'métadonnée',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('insee', models.CharField(max_length=2, validators=[django.core.validators.RegexValidator('^\\d\\d$')], verbose_name='identifiant Insee')),
                ('siren', models.CharField(blank=True, max_length=9, null=True, validators=[francedata.services.validators.validate_siren], verbose_name='numéro Siren')),
                ('category', models.CharField(blank=True, choices=[('REG', 'Région'), ('CTU', 'Collectivité territoriale unique')], max_length=3, null=True, verbose_name='catégorie')),
                ('slug', models.CharField(blank=True, default='', max_length=100)),
                ('years', models.ManyToManyField(to='francedata.DataYear', verbose_name='millésimes')),
            ],
            options={
                'verbose_name': 'région',
            },
        ),
        migrations.CreateModel(
            name='RegionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('datacode', models.CharField(max_length=255, verbose_name='code')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='valeur')),
                ('datatype', models.CharField(blank=True, max_length=255, null=True, verbose_name='type')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='francedata.region', verbose_name='région')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datasource', verbose_name='source')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datayear', verbose_name='millésime')),
            ],
            options={
                'verbose_name': 'donnée région',
                'verbose_name_plural': 'données région',
            },
        ),
        migrations.CreateModel(
            name='EpciData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('datacode', models.CharField(max_length=255, verbose_name='code')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='valeur')),
                ('datatype', models.CharField(blank=True, max_length=255, null=True, verbose_name='type')),
                ('epci', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='francedata.epci', verbose_name='EPCI')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datasource', verbose_name='source')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datayear', verbose_name='millésime')),
            ],
            options={
                'verbose_name': 'donnée EPCI',
                'verbose_name_plural': 'données EPCI',
            },
        ),
        migrations.CreateModel(
            name='DepartementData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('datacode', models.CharField(max_length=255, verbose_name='code')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='valeur')),
                ('datatype', models.CharField(blank=True, max_length=255, null=True, verbose_name='type')),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='francedata.departement', verbose_name='département')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datasource', verbose_name='source')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datayear', verbose_name='millésime')),
            ],
            options={
                'verbose_name': 'donnée département',
                'verbose_name_plural': 'données département',
            },
        ),
        migrations.AddField(
            model_name='departement',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='francedata.region', verbose_name='région'),
        ),
        migrations.AddField(
            model_name='departement',
            name='years',
            field=models.ManyToManyField(to='francedata.DataYear', verbose_name='millésimes'),
        ),
        migrations.AddField(
            model_name='datasource',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='francedata.datayear', verbose_name='millésime'),
        ),
        migrations.CreateModel(
            name='CommuneData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('datacode', models.CharField(max_length=255, verbose_name='code')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='valeur')),
                ('datatype', models.CharField(blank=True, max_length=255, null=True, verbose_name='type')),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='francedata.commune', verbose_name='commune')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datasource', verbose_name='source')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francedata.datayear', verbose_name='millésime')),
            ],
            options={
                'verbose_name': 'donnée commune',
                'verbose_name_plural': 'données commune',
            },
        ),
        migrations.AddField(
            model_name='commune',
            name='departement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='francedata.departement', verbose_name='département'),
        ),
        migrations.AddField(
            model_name='commune',
            name='epci',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='francedata.epci', verbose_name='EPCI'),
        ),
        migrations.AddField(
            model_name='commune',
            name='years',
            field=models.ManyToManyField(to='francedata.DataYear', verbose_name='millésimes'),
        ),
        migrations.AddConstraint(
            model_name='regiondata',
            constraint=models.UniqueConstraint(fields=('region', 'year', 'datacode'), name='fd_unique_region_data'),
        ),
        migrations.AlterUniqueTogether(
            name='region',
            unique_together={('name', 'insee')},
        ),
        migrations.AddConstraint(
            model_name='epcidata',
            constraint=models.UniqueConstraint(fields=('epci', 'year', 'datacode'), name='fd_unique_epci_data'),
        ),
        migrations.AddConstraint(
            model_name='departementdata',
            constraint=models.UniqueConstraint(fields=('departement', 'year', 'datacode'), name='fd_unique_departement_data'),
        ),
        migrations.AlterUniqueTogether(
            name='datasource',
            unique_together={('title', 'url', 'year')},
        ),
        migrations.AddConstraint(
            model_name='communedata',
            constraint=models.UniqueConstraint(fields=('commune', 'year', 'datacode'), name='fd_unique_commune_data'),
        ),
    ]
