# Generated by Django 2.0.3 on 2018-04-14 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_auto_20180414_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notify_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='triggered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='triggered_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
