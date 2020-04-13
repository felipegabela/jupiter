# Generated by Django 3.0.2 on 2020-03-26 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production_scheduler', '0007_seamstress_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seamstress',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]