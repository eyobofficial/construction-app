from django.db import models


class ProjectManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super(ProjectManager, self).get_queryset().filter(
            is_published=True
        )

    def active(self, *args, **kwargs):
        return self.get_queryset().filter(
            status='active'
        )

    def closed(self, *args, **kwargs):
        return self.get_queryset().filter(
            status='closed'
        )

    def defect(self, *args, **kwargs):
        return self.get_queryset().filter(
            status='defect'
        )

    def suspended(self, *args, **kwargs):
        return self.get_queryset().filter(
            status='suspended'
        )

    def terminated(self, *args, **kwargs):
        return self.get_queryset().filter(
            status='terminated'
        )

