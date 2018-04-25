from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        # from .signals import project_status_notifications
        from .signals import new_project_notifications

