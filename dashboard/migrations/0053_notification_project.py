# Generated by Django 2.0.3 on 2018-04-23 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0052_remove_notification_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='dashboard.Project'),
        ),
    ]
