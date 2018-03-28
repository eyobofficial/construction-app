from django.db import models


class ProjectManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super(ProjectManager, self).get_queryset().filter(
            is_published=True
        )

    def unknown(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=1
        )

    def mobilization(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=2
        )

    def active(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=3
        )

    def rectification(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=4
        )

    def suspended(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=5
        )

    def terminated(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=6
        )

    def closed(self, *args, **kwargs):
        return self.get_queryset().filter(
            status=7
        )

