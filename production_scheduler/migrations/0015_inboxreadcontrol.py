# Generated by Django 3.0.2 on 2020-04-22 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production_scheduler', '0014_lineitem_fecha_assignacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='InboxReadControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_event_viewed_date', models.DateTimeField()),
                ('line_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_scheduler.LineItem')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]