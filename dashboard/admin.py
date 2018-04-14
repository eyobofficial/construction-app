from django.contrib import admin
from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'get_full_name',
        'date_joined',
        'last_login',
        'is_active',
    )
    list_filter = ('is_active', )
    search_fields = ('email', 'username', 'first_name', 'last_name', )


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'config_type', )
    list_filter = ('config_type', )
    search_fields = ('name', 'value', )


@admin.register(models.Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name', )
    search_fields = ('full_name', 'short_name')


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'consultant', 'construction_type', 'status',)
    list_filter = ('construction_type', 'consultant', 'status')
    search_fields = ('full_name', 'short_name', 'project_code', 'description',)


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'notification_type',
        'notification_title',
        'project',
        'triggered_by',
        'notify_to',
        'is_seen',
        'is_email_sent'
    )
    list_filter = (
        'notification_type',
        'project',
        'triggered_by',
        'is_seen',
        'is_email_sent'
    )
    search_fields = ('notification_title', 'notification_text', )


