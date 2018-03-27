from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings

from . import managers

import datetime


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    job_title = models.CharField(max_length=100)
    bio = models.TextField('Short Bio', null=True, blank=True)
    projects_followed = models.ManyToManyField(
        'Project',
        related_name='projects_followed',
        blank=True
    )
    projects_administered = models.ManyToManyField(
        'Project',
        related_name='projects_administered',
        blank=True
    )
    is_project_admin = models.BooleanField(
        'Admin Project Detals',
        default=False,
    )
    is_insurance_admin = models.BooleanField(
        'Admin Insurance Details',
        default=False,
    )
    is_variation_admin = models.BooleanField(
        'Admin Variation Details',
        default=False,
    )
    is_claim_admin = models.BooleanField(
        'Admin Time Claim Details',
        default=False,
    )
    is_payment_admin = models.BooleanField(
        'Admin Payment Details',
        default=False,
    )


class Contractor(models.Model):
    """
    Represents a Contractor Firm
    """
    # package = models.ForeignKey(Package, on_delete=models.CASCADE)
    full_name = models.CharField(
        max_length=100,
        help_text='Official full name of the Contractor firm',
    )
    short_name = models.CharField(
        max_length=100,
        help_text='Short common name of the Contractor firm',
    )
    description = models.TextField(
        null=True, blank=True,
        help_text='Short description of the Contractor firm. (Optional)',
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('dashboard:contractor-detail', args=[str(self.pk)])

    def __str__(self):
        return self.short_name


class Consultant(models.Model):
    """
    Represents a Consultant Firm
    """
    full_name = models.CharField(
        max_length=100,
        help_text='Official full name of the Consultant firm',
    )
    short_name = models.CharField(
        max_length=100,
        help_text='Short common name of the Consultant firm',
    )
    description = models.TextField(
        null=True, blank=True,
        help_text='Short description of the Consultant firm. (Optional)',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('dashboard:consultant-detail', args=[str(self.pk)])

    def __str__(self):
        return self.short_name


class Project(models.Model):
    """
    Represents a Construction Project
    """
    CONSTRUCTION_TYPE_CHOICES = (
        ('builiding', 'Buildings and Structures'),
        ('road', 'Road and Highway'),
        ('water', 'Water and Irrigations'),
    )
    construction_type = models.CharField(
        max_length=60,
        choices=CONSTRUCTION_TYPE_CHOICES,
        default='builiding'
    )
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    employer = models.CharField(
        max_length=100,
        help_text='Official full name of the Employer',
    )
    full_name = models.CharField(
        'Official Project Title',
        max_length=100,
        help_text='Official full name of the construction project',
    )
    short_name = models.CharField(
        'Short Unofficial Project Title',
        max_length=100,
        help_text='Short common name of the construction project',
    )
    project_code = models.CharField(
        'Project Code (Optional)',
        max_length=30,
        null=True, blank=True,
    )
    description = models.TextField(
        'Short Project Description',
        null=True, blank=True,
        help_text='Short description of the construction project. (Optional)',
    )
    contract_amount = models.DecimalField(
        max_digits=16, decimal_places=2,
        null=True, blank=True,
        help_text='Project contract amount in ETB',
    )
    signing_date = models.DateField(
        'Agreement Signing Date',
        null=True, blank=True,
        help_text='User yyyy-mm-dd format',
    )
    site_handover = models.DateField(
        'Site Handover Date',
        null=True, blank=True,
        help_text='User yyyy-mm-dd format',
    )
    commencement_date = models.DateField(
        'Commenecment Date',
        null=True, blank=True,
        help_text='User yyyy-mm-dd format',
    )
    period = models.IntegerField(
        'Contract Period',
        null=True, blank=True,
        help_text='Project life time in calendar days')
    completion_date = models.DateField(
        'Intended Completion Date',
        null=True, blank=True,
        help_text='User yyyy-mm-dd format',
    )
    is_published = models.BooleanField('Published status', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom Managers
    objects = models.Manager()
    my_projects = managers.ProjectManager()

    def current_status(self):
        status_list = self.project_status.all().order_by('-updated_at')

        try:
            last_status = status_list[0].status
        except:
            last_status = None
        return last_status

    def save(self, *args, **kwargs):
        if self.commencement_date and self.period:
            self.completion_date = self.commencement_date+ datetime.timedelta(self.period)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dashboard:project-detail', args=[str(self.pk)])

    def __str__(self):
        return self.short_name


class ProjectStatus(models.Model):
    """
    Represents Project Status History
    """
    PROJECT_STATUS_CHOICES = (
        ('active', 'Active'),
        ('defect', 'Defect Liability Period'),
        ('closed', 'Closed'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    )
    project = models.ForeignKey(
        Project,
        related_name='project_status',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        'Project Status',
        max_length=60,
        choices=PROJECT_STATUS_CHOICES,
        default='active'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'project', ]

    def __str__(self):
        return 'Status of {}'.format(self.project)
