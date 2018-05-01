from django import forms
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
    filter_horizontal = ('projects_followed', 'projects_administered', )


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
        'project',
        'subject',
        'triggered_by',
        'notify_to',
        'is_seen',
        'is_email_sent',
        'content_object',
        'created_at',
    )
    list_display_links = ('subject', )
    list_filter = ('project', 'is_seen', 'is_email_sent', )
    search_fields = ('subject', 'message', )


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
    fields = ('week', 'amount', 'activities', 'updated_at', )
    readonly_fields = ('updated_at', )
    filter_horizontal = ('activities', )
    extra = 0


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project',
        'is_active',
        'no_of_weeks',
        'updated_at',
    )
    list_filter = ('is_active', 'project', )
    search_fields = ('title', )
    inlines = (PlanInline, )

    def no_of_weeks(self, obj):
        return obj.plans.count()


class ProgressForm(forms.ModelForm):
    WEEK_CHOICE = (
        ('Week 1', 1),
        ('Week 2', 2),
        ('Week 3', 3),
    )
    week = forms.ChoiceField(choices=WEEK_CHOICE)

    class Meta:
        model = models.Progress
        fields = [
            'project', 'week', 'amount',
            'activities', 'description', 'slippage_reason', 'remark',
        ]


@admin.register(models.Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('project', 'week', 'amount', )
    # form = ProgressForm
    filter_horizontal = ('activities', )
