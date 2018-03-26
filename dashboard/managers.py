from django.db import models


class ProjectManager(models.Manager):

    def get_queryset(self, user, *args, **kwargs):
        return super(ProjectManager, self).get_queryset().filter(
            contractor=user.profile.contractor
        )

    def all(self, user):
        return self.get_queryset(user)

    def active(self, user, *args, **kwargs):
        return self.get_queryset(user).filter(
            status='active'
        )

    def closed(self, user, *args, **kwargs):
        return self.get_queryset(user).filter(
            status='closed'
        )

    def defect(self, user, *args, **kwargs):
        return self.get_queryset(user).filter(
            status='defect'
        )

    def suspended(self, user, *args, **kwargs):
        return self.get_queryset(user).filter(
            status='suspended'
        )

    def terminated(self, user, *args, **kwargs):
        return self.get_queryset(user).filter(
            status='terminated'
        )

