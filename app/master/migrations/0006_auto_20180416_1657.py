# Generated by Django 2.0.4 on 2018-04-16 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_auto_20180415_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paises', to='master.Item'),
        ),
    ]
