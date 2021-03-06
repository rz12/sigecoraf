# Generated by Django 2.0.2 on 2018-02-24 05:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25, unique=True)),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(max_length=500)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle_principal', models.TextField(max_length=500)),
                ('calle_secundaria', models.TextField(blank=True, max_length=500, null=True)),
                ('ciudad', models.CharField(max_length=250)),
                ('referencia', models.TextField(blank=True, max_length=500, null=True)),
                ('numero_telefono', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(max_length=500)),
                ('estado', models.BooleanField(default=True)),
                ('logo', models.FileField(null=True, upload_to='')),
                ('autorizacion_sri', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25, unique=True)),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(max_length=500)),
                ('estado', models.BooleanField(default=True)),
                ('catalogo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='master.Catalogo')),
                ('padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Item')),
            ],
        ),
        migrations.AlterField(
            model_name='persona',
            name='foto',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='direccion',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.Item'),
        ),
        migrations.AddField(
            model_name='direccion',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direcciones', to='master.Persona'),
        ),
        migrations.AddField(
            model_name='direccion',
            name='tipo_direccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipo_direccion', to='master.Item'),
        ),
        migrations.AddField(
            model_name='catalogo',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalogos', to='master.Empresa'),
        ),
        migrations.AddField(
            model_name='persona',
            name='estado_civil',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='estado_civil', to='master.Item'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='genero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='genero', to='master.Item'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='tipo_documento_identificacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_documento_identificacion', to='master.Item'),
            preserve_default=False,
        ),
    ]
