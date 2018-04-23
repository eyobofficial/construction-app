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


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'triggered_by',
        'content_object',
        'project',
        'created_at',
    )
    list_display_links = ('subject', )
    search_fields = ('subject', 'message', )


@admin.register(models.UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('notify_to', 'notification', 'is_seen', 'is_email_sent', 'created_at', )
    list_display_links = ('notification', )
    list_filter = ('is_seen', 'is_email_sent')
    search_fields = ('notification', )


admin.site.register(models.Activity)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'consultant', 'construction_type', 'status',)
    list_filter = ('construction_type', 'consultant', 'status')
    exclude = ('created_by', )
    search_fields = ('full_name', 'short_name', 'project_code', 'description',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class PlanInline(admin.StackedInline):
    model = models.Plan
    list_display = (
        'schedule_project',
        'schedule',
        'period_start_date',
        'amount',
    )


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'period', 'is_active', 'updated_at', )
    list_filter = ('is_active', 'project', )
    search_fields = ('title', )
    inlines = (PlanInline, )


@admin.register(models.Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('plan', 'amount', )
