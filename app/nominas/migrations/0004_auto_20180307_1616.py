# Generated by Django 2.0.3 on 2018-03-07 21:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0003_auto_20180227_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsolidadoRolPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_desde', models.DateField(auto_now_add=True)),
                ('fecha_hasta', models.DateField(auto_now_add=True)),
                ('observacion', models.TextField(blank=True, max_length=500, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='rolpago',
            name='consolidado_rolpago',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='roles_pago', to='nominas_report.ConsolidadoRolPago'),
            preserve_default=False,
        ),
    ]
