from django.shortcuts import render
from django.views import generic

from dashboard import models


class ProjectList(generic.ListView):
    """
    List all published projects
    """
    model = models.Project
    template_name = 'dashboard/projects/project_list.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.my_projects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context
