# Generated by Django 2.0.3 on 2018-03-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20180327_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Published status'),
        ),
    ]