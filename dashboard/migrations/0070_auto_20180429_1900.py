# Generated by Django 2.0.3 on 2018-04-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0069_auto_20180429_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='week',
            field=models.PositiveSmallIntegerField(verbose_name='Week Number'),
        ),
        migrations.AlterUniqueTogether(
            name='plan',
            unique_together={('schedule', 'week')},
        ),
    ]