# Generated by Django 2.0.3 on 2018-04-17 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0006_auto_20180417_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallerolpago',
            name='cantidad',
            field=models.TextField(blank=True, null=True),
        ),
    ]
