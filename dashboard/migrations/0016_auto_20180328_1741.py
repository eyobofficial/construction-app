# Generated by Django 2.0.3 on 2018-03-28 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_config'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config',
            options={'ordering': ['config_type'], 'verbose_name': 'Website Configuration', 'verbose_name_plural': 'Website Configurations'},
        ),
        migrations.RenameField(
            model_name='config',
            old_name='config_types',
            new_name='config_type',
        ),
        migrations.RemoveField(
            model_name='project',
            name='contractor',
        ),
        migrations.DeleteModel(
            name='Contractor',
        ),
    ]
