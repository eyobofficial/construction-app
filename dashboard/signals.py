from django.db.models import signals
from django.dispatch import receiver

from . import models


@receiver(signals.post_save, sender=models.Project)
def add_project_notifications(sender, instance, created, **kwargs):
    if created:
        notification_title = '[New Project] {} Construction Project'.format(
            instance.short_name
        )
        notification_body = """
        {} construction project is created by {} on {}.
        """.format(
            instance.full_name,
            instance.created_by.get_screen_name(),
            instance.created_at,
        )
        instance.add_notification(
            notification_title, notification_body,
            broadcast=True,
        )


@receiver(signals.post_save, sender=models.Notification)
def create_user_notifications(sender, created, instance, **kwargs):
    """
    Everytime a Notification model is saved, create UserNotification to
    all users (except the trigger) that follow that project
    """
    if created:
        if instance.is_broadcast:
            project_followers = models.CustomUser.objects.filter(
                is_active=True
            )
        else:
            project_followers = instance.project.project_followers.all()

        if instance.triggered_by:
            project_followers = project_followers.exclude(
                pk=instance.triggered_by.pk
            )

        for user in project_followers:
            notification = instance.user_notifications.create(notify_to=user)
            notification.save()

