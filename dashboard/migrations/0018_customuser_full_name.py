# Generated by Django 2.0.3 on 2018-04-01 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_config_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]
