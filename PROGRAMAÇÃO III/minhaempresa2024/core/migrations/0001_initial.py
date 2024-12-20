# Generated by Django 4.2.16 on 2024-10-18 00:23

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('foto', stdimage.models.StdImageField(force_min_size=False, upload_to='equipe', variations={'thumb': {'crop': True, 'height': 500, 'width': 500}})),
                ('facebook', models.CharField(blank=True, max_length=150, null=True)),
                ('twitter', models.CharField(blank=True, max_length=150, null=True)),
                ('cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.cargo')),
            ],
            options={
                'verbose_name': 'funcionário',
                'verbose_name_plural': 'funcionários',
            },
        ),
    ]
