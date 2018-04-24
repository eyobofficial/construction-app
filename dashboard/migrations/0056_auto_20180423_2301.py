# Generated by Django 2.0.3 on 2018-04-23 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0055_notification_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_notifications', to='dashboard.Project'),
        ),
    ]