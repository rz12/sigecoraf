# Generated by Django 2.0.2 on 2018-02-27 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_auto_20180224_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleParametrizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25, unique=True)),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('valor', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Parametrizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=25, unique=True)),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parametrizaciones', to='master.Empresa')),
            ],
        ),
        migrations.AlterField(
            model_name='catalogo',
            name='descripcion',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='detalleparametrizacion',
            name='parametrizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='master.Parametrizacion'),
        ),
    ]
