from django.shortcuts import render
from django.views import generic

from dashboard import models

from dashboard import forms


def index(request):
    template_name = 'dashboard/index.html'
    return render(request, template_name, {})


class ProjectList(generic.ListView):
    """
    List all published projects
    """
    model = models.Project
    template_name = 'dashboard/projects/project_list.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.my_projects.all().order_by('status')

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context


class ProjectDetail(generic.DetailView):
    """
    Display  a single published project
    """
    model = models.Project
    template_name = 'dashboard/projects/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context


class ProjectCreate(generic.CreateView):
    """
    Create a new project record
    """
    form_class = forms.ProjectForm
    model = models.Project
    template_name = 'dashboard/projects/project_form.html'
    success_message = 'New project created successfully.'


    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context
