# Generated by Django 2.0.2 on 2018-02-27 20:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_auto_20180227_1512'),
        ('nominas', '0002_auto_20180224_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('sueldo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='master.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(default=datetime.date.today)),
                ('fecha_fin', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('mensualizar_decimos', models.NullBooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRolPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='EstructuraDetalleRolPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('operacion', models.IntegerField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estructuras_detalles_rolpago', to='master.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='RolPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.AlterField(
            model_name='empleado',
            name='fecha_fin',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='fecha_ingreso_iess',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AddField(
            model_name='detallerolpago',
            name='estructura_detalle_rolpago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='nominas_report.EstructuraDetalleRolPago'),
        ),
        migrations.AddField(
            model_name='detallerolpago',
            name='rol_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='nominas_report.RolPago'),
        ),
    ]
