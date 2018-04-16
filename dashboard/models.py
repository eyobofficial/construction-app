from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.mail import EmailMessage, get_connection
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

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('dashboard:consultant-detail', args=[str(self.pk)])


class Notification(models.Model):
    """
    Represents a Notification
    """
    NOTIFICATION_TYPE_CHOICES = (
        ('alert', 'Alert'),
        ('warning', 'Warning'),
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
        on_delete=models.SET_NULL,
        related_name='triggered_notifications'
    )
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=255)
    is_broadcast = models.BooleanField(
        default=False,
        help_text='Send notification to all users'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'project', 'notification_type', ]

    def __str__(self):
        return self.title

    def get_redirect_url(self, *args, **kwargs):
        """
        Returns a URL for the notification link to redirect to
        """
        # Temporary solution
        return self.project.get_absolute_url()

    def get_email_subject(self, *args, **kwargs):
        """
        Return a 'Subject' for email of this notification
        """
        subject = '[{}] - {}'.format(
            self.get_notification_type_display(),
            self.title
        )
        return subject

    def get_email_body(self, *args, **kwargs):
        """
        Returns the 'Body' of the email for this notification
        """
        email_body = '''
        {} CONSTRUCTION PROJECT

        {}
        {}
        '''.format(
            self.project.short_name.upper(),
            self.body,
            self.get_redirect_url(),
        )
        return email_body

    def send_emails(self, *args, **kwargs):
        user_notifications = self.user_notifications.filter(
            is_email_sent=False
        )
        connection = get_connection()
        connection.open()

        for notification in user_notifications:
            email_messaage = notification.get_email_message(
                connection=connection
            )
            if email_messaage.send():
                notification.is_email_sent = True
                notification.save()
        connection.close()

    @staticmethod
    def send_unsent_emails(**kwargs):
        triggered_by = kwargs.get('triggered_by')
        notify_to = kwargs.get('notify_to')

        query = Notification.objects.filter(is_email_sent=False)

        if triggered_by:
            query = query.filter(triggered_by=triggered_by)

        if notify_to:
            query = query.filter(notify_to=notify_to)

        for notification in query:
            notification.send_email_notification()


class UserNotification(models.Model):
    """
    Represents a User Notification
    """
    notification = models.ForeignKey(
        Notification,
        related_name='user_notifications',
        on_delete=models.CASCADE
    )
    notify_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    is_seen = models.BooleanField('Seen', default=False)
    seen_date = models.DateTimeField(null=True, blank=True)
    is_email_sent = models.BooleanField('Email Sent Status', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_seen', 'notification', ]
        get_latest_by = ['seen_date', ]

    def __str__(self, *args, **kwargs):
        return '{} -> {}'.format(self.notification, self.notify_to)

    def get_email_message(self, *args, **kwargs):
        """
        Returns a EmailMessage object
        """
        connection = kwargs.get('connection')
        subject = self.notification.get_email_subject()
        body = self.notification.get_email_body()
        sender = settings.EMAIL_HOST_USER
        recipient_list = [self.notify_to.email, ]
        return EmailMessage(
            subject,
            body,
            sender,
            recipient_list,
            connection=connection
        )

    def send_email(self, *args, **kwargs):
        email_message = self.get_email_message()
        if email_message.send():
            self.is_email_sent = True
            self.save()


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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom Managers
    objects = models.Manager()
    my_projects = managers.ProjectManager()

    class Meta:
        ordering = ['status', '-updated_at', 'short_name', ]
        get_latest_by = 'updated_at'
        permissions = (
            ('admin_project', 'Administer Project'),
        )

    def __str__(self):
        return self.short_name

    def get_original_completion_date(self, *args, **kwargs):
        """
        Returns the project completion date
        """
        if self.commencement_date and self.period:
            return self.commencement_date + datetime.timedelta(days=self.period)
        return

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

    def get_absolute_url(self):
        return reverse('dashboard:project-detail', args=[str(self.pk)])

