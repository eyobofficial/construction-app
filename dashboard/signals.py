from django.db.models import signals
from django.dispatch import receiver

from . import models


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
            ).exclude(pk=instance.triggered_by.pk)
        else:
            project_followers = instance.project.project_followers.exclude(
                pk=instance.triggered_by.pk
            )

        for user in project_followers:
            notification = instance.user_notifications.create(notify_to=user)
            notification.save()


