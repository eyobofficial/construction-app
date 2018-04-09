from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from . import utils

from . import managers

import datetime


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    full_name = models.CharField(max_length=120)
    job_title = models.CharField(max_length=100)
    bio = models.TextField('Short Bio', null=True, blank=True)
    projects_followed = models.ManyToManyField(
        'Project',
        related_name='project_followers',
        blank=True
    )
    projects_administered = models.ManyToManyField(
        'Project',
        related_name='projects_admins',
        blank=True
    )
    is_project_admin = models.BooleanField(
        'Administer Project Detals',
        default=False,
    )
    is_insurance_admin = models.BooleanField(
        'Administer Insurance Details',
        default=False,
    )
    is_variation_admin = models.BooleanField(
        'Administer Variation Details',
        default=False,
    )
    is_claim_admin = models.BooleanField(
        'Administer Time Claim Details',
        default=False,
    )
    is_payment_admin = models.BooleanField(
        'Administer Payment Details',
        default=False,
    )

    def get_full_name(self):
        return self.full_name 

    def get_screen_name(self):
        """
        Returns either the user's full name (if is set) or their username
        """
        if self.full_name:
            return self.get_full_name()
        else:
            return self.username


class Config(models.Model):
    """
    Constant configurations and meta data
    """
    CONFIG_TYPE_CHOICES = (
        ('company', 'Company detail configurations'),
        ('website', 'Website configurations'),
        ('other', 'Other configurations'),
    )
    config_type = models.CharField(
        max_length=60,
        choices=CONFIG_TYPE_CHOICES,
    )
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60)
    value = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['config_type', ]
        verbose_name = 'Website Configuration'
        verbose_name_plural = 'Website Configurations'

    def __str__(self):
        return self.name


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


class Notification(models.Model):
    """
    Represents a Notification
    """
    NOTIFICATION_TYPE_CHOICES = (
        ('info', 'Information'),
        ('warning', 'Warnining'),
    )
    notification_type = models.CharField(
        max_length=100,
        choices=NOTIFICATION_TYPE_CHOICES,
    )
    project = models.ForeignKey(
        'Project',
        null=True,
        on_delete=models.CASCADE
    )
    triggered_by = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL
    )
    notification_text = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=100)
    email_text = models.TextField(null=True, blank=True)
    notification_url = models.URLField()
    is_broadcast = models.BooleanField('Broadcast to all users', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'project', 'notification_type', ]

    def __str__(self):
        return self.notification_text


class UserNotification(models.Model):
    """
    Notifications for based projects followed by users
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_seen = models.BooleanField('Seen', default=False)
    seen_date = models.DateTimeField(null=True)

    def send_email(self, *args, **kwargs):
        return send_mail(
            self.notification.email_subject,
            self.notification.email_text,
            settings.EMAIL_HOST_USER,
            [self.user.email, ],
        )

    def __str__(self):
        return '{} for {}'.format(self.notification, self.user)


class Project(models.Model):
    """
    Represents a Construction Project
    """
    CONSTRUCTION_TYPE_CHOICES = (
        ('builiding', 'Buildings and Structures'),
        ('road', 'Road and Highway'),
        ('water', 'Water and Irrigations'),
    )
    PROJECT_STATUS_CHOICES = (
        (1, 'Unknown'),
        (2, 'Mobilization'),
        (3, 'Active'),
        (4, 'Rectification'),
        (5, 'Suspended'),
        (6, 'Terminated'),
        (7, 'Closed'),
    )
    PUBLISHED_STATUS_CHOICES = (
        (True, 'Published'),
        (False, 'Draft'),
    )
    construction_type = models.CharField(
        max_length=60,
        choices=CONSTRUCTION_TYPE_CHOICES,
        default='builiding'
    )
    status = models.IntegerField(
        'Project Status',
        choices=PROJECT_STATUS_CHOICES,
        default=1,
    )
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
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
        help_text='Project contract amount in ETB (before VAT)',
    )
    signing_date = models.DateField(
        'Agreement Signing Date',
        null=True, blank=True,
    )
    site_handover = models.DateField(
        'Site Handover Date',
        null=True, blank=True,
    )
    commencement_date = models.DateField(
        'commencement Date',
        null=True, blank=True,
    )
    period = models.PositiveIntegerField(
        'Contract Period',
        null=True, blank=True,
        help_text='Project life time in calendar days')
    completion_date = models.DateField(
        'Intended Completion Date',
        null=True, blank=True,
        help_text='User yyyy-mm-dd format',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom Managers
    objects = models.Manager()
    my_projects = managers.ProjectManager()

    class Meta:
        ordering = ['status', '-updated_at', 'short_name', ]
        permissions = (
            ('admin_project', 'Administer Project'),
        )

    def get_status_label(self):
        """
        Returns a bootstrap label for status
        """
        if self.status == 2:
            return utils.status_label(
                btn='badge-primary',
                status=self.get_status_display()
            )
        elif self.status == 3:
            return utils.status_label(
                btn='badge-success',
                status=self.get_status_display()
            )
        elif self.status == 4:
            return utils.status_label(
                btn='badge-info',
                status=self.get_status_display()
            )
        elif self.status == 5:
            return utils.status_label(
                btn='badge-warning',
                status=self.get_status_display()
            )
        elif self.status == 6:
            return utils.status_label(
                btn='badge-danger',
                status=self.get_status_display()
            )
        else:
            return utils.status_label(
                btn='badge-default',
                status=self.get_status_display()
            )

    def save(self, *args, **kwargs):
        if self.commencement_date and self.period:
            self.completion_date = self.commencement_date+ datetime.timedelta(self.period)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dashboard:project-detail', args=[str(self.pk)])

    def __str__(self):
        return self.short_name

