# Generated by Django 2.0.3 on 2018-04-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_auto_20180408_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='commencement_date',
            field=models.DateField(blank=True, null=True, verbose_name='commencement Date'),
        ),
    ]
