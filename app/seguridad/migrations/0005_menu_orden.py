# Generated by Django 2.0.3 on 2018-04-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0004_auto_20180308_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='orden',
            field=models.IntegerField(blank=True, default=True, null=True),
        ),
    ]
