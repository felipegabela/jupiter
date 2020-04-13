# Generated by Django 3.0.2 on 2020-04-01 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production_scheduler', '0009_auto_20200325_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='status',
            field=models.IntegerField(choices=[(0, 'Nueva'), (1, 'Asignada'), (2, 'Cortando'), (3, 'Armando'), (4, 'Terminada'), (5, 'Entregada'), (6, 'Corregir Error'), (7, 'Corrigiendo')], default=0),
        ),
    ]