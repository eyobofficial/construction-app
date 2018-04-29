# Generated by Django 2.0.3 on 2018-04-27 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0064_auto_20180427_0852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'get_latest_by': ['-start_date', '-updated_at'], 'ordering': ['schedule', 'start_date'], 'permissions': (('admin_plan', 'Administer Plans'),), 'verbose_name': 'Schedule Plan', 'verbose_name_plural': 'Schedule Plans'},
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='period_start_date',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='period',
        ),
    ]