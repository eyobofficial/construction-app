from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.utils import timezone
from model_utils import FieldTracker
from . import utils
from . import managers

import datetime


class Base(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Record created date and time'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Record last updated date and time'
    )

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    full_name = models.CharField(max_length=120)
    job_title = models.CharField(max_length=100)
    bio = models.TextField('Short Bio', null=True, blank=True)
    projects_followed = models.ManyToManyField(
        'Project',
        related_name='followers',
        blank=True
    )
    projects_administered = models.ManyToManyField(
        'Project',
        related_name='admins',
        blank=True
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

    def get_notifications(self, *args, **kwargs):
        """
        Returns all notification received by this user instance
        """
        return self.received_notifications.order_by('-created_at')

    def unseen_notifications(self, *args, **kwargs):
        return self.received_notifications.filter(is_seen=False)


class Config(Base):
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

    class Meta:
        ordering = ['config_type', ]
        verbose_name = 'Website Configuration'
        verbose_name_plural = 'Website Configurations'

    def __str__(self):
        return self.name


class Consultant(Base):
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

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('dashboard:consultant-detail', args=[str(self.pk)])


class Notification(Base):
    """
    Represents a Notification
    """
    project = models.ForeignKey(
        'Project',
        related_name='all_notifications',
        on_delete=models.CASCADE,
    )
    triggered_by = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL,
        related_name='triggered_notifications'
    )
    notify_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    subject = models.CharField(max_length=120)
    message = models.TextField('Notification message')
    is_seen = models.BooleanField('Seen', default=False)
    seen_date = models.DateTimeField(null=True, blank=True)
    is_email_sent = models.BooleanField('Email Sent Status', default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        ordering = ['-is_seen', '-updated_at', ]
        get_latest_by = ['-updated_at', ]

    def __str__(self):
        return '{} - From {} To {}'.format(
            self.subject,
            self.triggered_by,
            self.notify_to
        )

    def get_email_subject(self, *args, **kwargs):
        """
        Return a 'Subject' for email of this notification
        """
        return self.subject

    def get_email_body(self, *args, **kwargs):
        """
        Returns the 'Body' of the email for this notification
        """
        return self.message

    def get_email_message(self, *args, **kwargs):
        """
        Returns a EmailMessage object
        """
        connection = kwargs.get('connection')
        subject = self.notification.get_email_subject()
        body = self.get_email_body()
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
            notification.send_email()


class Activity(Base):
    """
    Represents construction Activity
    Example: Earth works, Concrete Work, Finishing Work
    """
    title = models.CharField('Construction Activity', max_length=60)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['title', 'updated_at', ]
        verbose_name = 'Construction Activity'
        verbose_name_plural = 'Construction Activities'

    def __str__(self):
        return self.title


class Project(Base):
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
    commencement_date = models.DateField('commencement Date')
    period = models.PositiveIntegerField(
        'Contract Period',
        help_text='Project life time in calendar days'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='projects',
        on_delete=models.SET(utils.get_phantom_user),
    )
    notifications = GenericRelation(Notification)

    # Field Tracker module
    tracker = FieldTracker()

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

    def get_absolute_url(self):
        return reverse('dashboard:project-detail', args=[str(self.pk)])

    @property
    def completion_date(self, *args, **kwargs):
        """
        Returns the project completion date
        """
        return self.commencement_date + datetime.timedelta(days=self.period)

    def get_days_left(self, *args, **kwargs):
        """
        Returns the number of days left to project completion date in
        calendar days
        """
        return (self.completion_date - timezone.localdate()).days

    def add_notification(self, subject, message, notify_to, *args, **kwargs):
        triggered_by = kwargs.get('triggered_by')
        self.notifications.create(
            project=self,
            triggered_by=triggered_by,
            notify_to=notify_to,
            subject=subject,
            message=message,
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


class Schedule(Base):
    """
    Represents a construction working schedule
    """
    project = models.ForeignKey(
        Project,
        related_name='schedules',
        on_delete=models.CASCADE
    )
    title = models.CharField('Schedule Title', max_length=120)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField('Active Status', default=False)
    start_date = models.DateField('Schedule Start Date')
    end_date = models.DateField('Schedule End Date')

    class Meta:
        ordering = ['is_active', 'project', '-updated_at', ]
        get_latest_by = ['updated_at', ]
        permissions = (
            ('admin_schedule', 'Administer Schedule'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse('dashboard:schedule-detail', args=[str(self.pk)])

    def get_week_count(self, *args, **kwargs):
        pass


class Plan(Base):
    """
    Represents a planned amount for a period (i.e. week)
    """
    schedule = models.ForeignKey(
        Schedule,
        related_name='plans',
        on_delete=models.CASCADE
    )
    week = models.PositiveIntegerField('Week Number', unique=True)
    amount = models.DecimalField(
        'Planned Amount',
        max_digits=12,
        decimal_places=2,
        default=0.0
    )
    activities = models.ManyToManyField(
        Activity,
        blank=True,
        verbose_name='Planned Activities',
        related_name='activity_plans',
    )

    class Meta:
        ordering = ['schedule', 'week', ]
        get_latest_by = ['-updated_at', ]
        permissions = (
            ('admin_plan', 'Administer Plans'),
        )
        verbose_name = 'Schedule Plan'
        verbose_name_plural = 'Schedule Plans'

    def __str__(self):
        return '{} Plan for {}'.format(self.start_date, self.schedule)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('dashboard:plan-detail', args=[str(self.pk)])

    def get_date_range(self, *args, **kwargs):
        pass

    def get_start_date(self, *args, **kwargs):
        pass

    def get_end_date(self, *args, **kwargs):
        pass


class Progress(Base):
    """
    Represents planned vs executed amount progress for a period
    """
    plan = models.ForeignKey(
        Plan,
        related_name='progress_list',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        'Executed Amount',
        max_digits=12,
        decimal_places=2,
        default=0.0
    )
    activities = models.ManyToManyField(
        Activity,
        blank=True,
        verbose_name='Executed Activities',
        related_name='activity_reports',
    )
    description = models.TextField(
        'Description of executed works',
        null=True, blank=True,
    )
    slippage_reason = models.TextField(
        'Reasons and descrioption of slippage',
        null=True, blank=True,
    )
    remark = models.TextField(
        'Additional Notes and Remarks',
        null=True, blank=True,
    )

    class Meta:
        ordering = ['plan', '-updated_at', ]
        get_latest_by = ['-updated_at', ]
        permissions = (
            ('admin_progress', 'Administer Progress'),
        )

    def __str__(self):
        return 'Report for {}'.format(self.plan)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('dashboard:report-detail', args=[str(self.pk)])

    def get_slippage_amount(self, *args, **kwargs):
        pass

    def get_slippage_percentage(self, *args, **kwargs):
        pass


class Payment(Base):
    """
    Represents a Payment Certificate (But not Subcontractor Payment)
    """
    PAYMENT_TYPE_CHOICES = (
        ('advance', 'Advance Payment'),
        ('interim', 'Interim Payment'),
        ('final', 'Final Payment'),
    )
    STATUS_CHOICES = (
        (1, 'Submitted'),
        (2, 'Under Correction'),
        (3, 'Approved'),
        (4, 'Rejected'),
    )
    project = models.ForeignKey(
        Project,
        related_name='payments',
        on_delete=models.CASCADE,
    )
    previous_payment = models.ForeignKey(
        'Payment',
        null=True, blank=True,
        related_name='next_payment',
        on_delete=models.SET_NULL,
    )
    payment_type = models.CharField(
        max_length=60,
        choices=PAYMENT_TYPE_CHOICES,
        default='interim',
    )
    status = models.IntegerField('Payment status')
    title = models.CharField('Payment title', max_length=100)
    service_sum = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0,
    )
    material_onsite = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0,
    )
    advance_repayment = models.DecimalField(
        'Advance repayment(%)',
        max_digits=5,
        decimal_places=2,
        default=30.0,
    )
    retention_repayment = models.DecimalField(
        'Retention repayment(%)',
        max_digits=5,
        decimal_places=2,
        default=5.0,
    )
    penality_repayment = models.DecimalField(
        'Penality repayment(%)',
        max_digits=5,
        decimal_places=2,
        default=0.0,
    )
    prepared_by = models.CharField(max_length=100, null=True, blank=True)
    submitted_date = models.DateField(null=True, blank=True)
    submitted_ref_no = models.CharField(
        'Submittal Letter Ref. No.',
        max_length=30,
        null=True, blank=True,
    )
    submitted_date = models.DateField(
        'Approval/Rejection date',
        null=True, blank=True
    )

    class Meta:
        ordering = ['project', 'previous_payment', ]
        get_latest_by = ['-updated_at', ]
        permissions = (
            ('admin_payment', 'Administer Payment'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse('dashboard:payment-detail', args=[str(self.pk)])

    def get_advance_repayment_amount(self, *args, **kwargs):
        pass

    def get_retention_repayment_amount(self, *args, **kwargs):
        pass

    def get_penality_amount(self, *args, **kwargs):
        pass

    def get_net_payment(self, *args, **kwargs):
        pass
