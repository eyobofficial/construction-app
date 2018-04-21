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


admin.site.register(models.Activity)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'consultant', 'construction_type', 'status',)
    list_filter = ('construction_type', 'consultant', 'status')
    search_fields = ('full_name', 'short_name', 'project_code', 'description',)


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'notification_type',
        'title',
        'project',
        'triggered_by',
    )
    list_filter = (
        'notification_type',
        'project',
        'triggered_by',
    )
    search_fields = ('title', 'body', )


@admin.register(models.UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('notify_to', 'notification', 'is_seen', 'is_email_sent')
    list_filter = ('is_seen', 'is_email_sent')
    search_fields = ('notification', )


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'period', 'is_active', 'updated_at', )
    list_filter = ('is_active', 'project', )
    search_fields = ('title', )


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'period_start_date', 'amount', )
    list_filter = ('schedule', )


@admin.register(models.Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('plan', 'amount', )
