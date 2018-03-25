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
