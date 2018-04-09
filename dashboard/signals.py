from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification, CustomUser, UserNotification


@receiver(post_save, sender=Notification)
def save_user_notification(sender, instance, created, **kwargs):
    project = instance.project

    if instance.is_broadcast:
        user_list = CustomUser.objects.filter(is_active=True)
    else:
        user_list = project.project_followers.filter(is_active=True)

    for user in user_list:
        if user is instance.triggered_by:
            continue

        user_notification = UserNotification.objects.create(
            notification=instance,
            user=user,
        )
        user_notification.save()
        # user_notification.send_email()


