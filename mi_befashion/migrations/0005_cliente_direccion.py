# Generated by Django 3.0.7 on 2020-09-18 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_befashion', '0004_auto_20200918_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, db_column='Dirección', max_length=255, null=True),
        ),
    ]
