# Generated by Django 2.0.3 on 2018-03-26 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Official full name of the Consultant firm', max_length=100)),
                ('short_name', models.CharField(help_text='Short common name of the Consultant firm', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Short description of the Consultant firm. (Optional)', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Official full name of the Contractor firm', max_length=100)),
                ('short_name', models.CharField(help_text='Short common name of the Contractor firm', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Short description of the Contractor firm. (Optional)', null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Job Title')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Short Bio')),
                ('contractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Contractor')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('construction_type', models.CharField(choices=[('builiding', 'Buildings and Structures'), ('road', 'Road and Highway'), ('water', 'Water and Irrigations')], default='builiding', max_length=60)),
                ('employer', models.CharField(help_text='Official full name of the Employer', max_length=100)),
                ('full_name', models.CharField(help_text='Official full name of the construction project', max_length=100, verbose_name='Official Project Title')),
                ('short_name', models.CharField(help_text='Short common name of the construction project', max_length=100, verbose_name='Short Unofficial Project Title')),
                ('project_code', models.CharField(blank=True, max_length=30, null=True, verbose_name='Project Code (Optional)')),
                ('description', models.TextField(blank=True, help_text='Short description of the construction project. (Optional)', null=True, verbose_name='Short Project Description')),
                ('contract_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Project contract amount in ETB', max_digits=16, null=True)),
                ('signing_date', models.DateField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Agreement Signing Date')),
                ('site_handover', models.DateField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Site Handover Date')),
                ('commencement_date', models.DateField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Commenecment Date')),
                ('period', models.IntegerField(blank=True, help_text='Project life time in calendar days', null=True, verbose_name='Contract Period')),
                ('completion_date', models.DateField(blank=True, help_text='User yyyy-mm-dd format', null=True, verbose_name='Intended Completion Date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Consultant')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Contractor')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('defect', 'Defect Liability Period'), ('closed', 'Closed'), ('suspended', 'Suspended'), ('closed', 'Closed')], default='active', max_length=60, verbose_name='Project Status')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Project')),
            ],
            options={
                'ordering': ['-updated_at', 'project'],
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_claim_admin',
            field=models.BooleanField(default=False, verbose_name='Admin Time Claim Details'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_insurance_admin',
            field=models.BooleanField(default=False, verbose_name='Admin Insurance Details'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_payment_admin',
            field=models.BooleanField(default=False, verbose_name='Admin Payment Details'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_project_admin',
            field=models.BooleanField(default=False, verbose_name='Admin Project Detals'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_variation_admin',
            field=models.BooleanField(default=False, verbose_name='Admin Variation Details'),
        ),
        migrations.AddField(
            model_name='projectstatus',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customuser',
            name='project_list',
            field=models.ManyToManyField(blank=True, to='dashboard.Project'),
        ),
    ]