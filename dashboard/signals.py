from django.db.models import signals
from django.dispatch import receiver

from . import models


@receiver(signals.pre_save, sender=models.Project)
def project_status_notifications(sender, instance, **kwargs):
    """
    Create project status changed notification when Project status is
    updated
    """
    # Check if project is already in the record
    is_not_new = instance.pk is not None

    if instance.tracker.has_changed('status') and is_not_new:
        subject = '{} Project Status Updated'.format(instance.short_name)
        message = '{} project status has been updated to {}'.format(
            instance.short_name,
            instance.get_status_display()
        )
        notify_list = instance.followers.filter(is_active=True)

        # Add notification
        for user in notify_list:
            instance.add_notification(subject, message, user)


@receiver(signals.post_save, sender=models.Project)
def new_project_notifications(sender, instance, created, **kwargs):
    """
    Create a notification when a new project is created
    """
    if created:
        subject = 'New Project Added - {}'.format(instance.full_name)
        message = 'A new project with the title {} has been added'.format(
            instance.full_name.title()
        )
        notify_list = models.CustomUser.objects.filter(is_active=True)

        # Add notification
        for user in notify_list:
            instance.add_notification(subject, message, user)
