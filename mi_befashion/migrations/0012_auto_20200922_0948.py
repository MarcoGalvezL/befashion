# Generated by Django 3.0.7 on 2020-09-22 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_befashion', '0011_integracionpago_fw_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='preventa',
            field=models.BooleanField(db_column='Pre venta', default=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='promocion',
            field=models.BooleanField(db_column='Promocion', default=False),
        ),
    ]
