# Generated by Django 2.0.3 on 2018-04-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0048_auto_20180421_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='activities',
            field=models.ManyToManyField(blank=True, related_name='activity_plans', to='dashboard.Activity', verbose_name='Planned Activities'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='activities',
            field=models.ManyToManyField(blank=True, related_name='activity_reports', to='dashboard.Activity', verbose_name='Executed Activities'),
        ),
    ]
