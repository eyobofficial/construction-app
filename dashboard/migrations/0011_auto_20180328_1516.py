# Generated by Django 2.0.3 on 2018-03-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20180328_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('mobilization', 'Mobilization'), ('active', 'Active'), ('rectification', 'Rectification'), ('closed', 'Closed'), ('suspended', 'Suspended'), ('terminated', 'Terminated')], default='unknown', max_length=60, verbose_name='Project Status'),
        ),
    ]