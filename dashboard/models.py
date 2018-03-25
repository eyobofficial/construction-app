from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from . import managers

import datetime


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    job_title = models.CharField(max_length=100)
    bio = models.TextField('Short Bio', null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    contractor = models.ForeignKey(
        'Contractor',
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField('Job Title', max_length=100)
    bio = models.TextField('Short Bio', null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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

