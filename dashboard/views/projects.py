from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from dashboard import models

from dashboard import forms

from dashboard import utils


@login_required
def index(request):
    template_name = 'dashboard/index.html'
    return render(request, template_name, {
        'page_name': 'index',
    })


class ProjectList(LoginRequiredMixin, generic.ListView):
    """
    List all published projects
    """
    model = models.Project
    template_name = 'dashboard/projects/project_list.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.my_projects.all().order_by('status')

    def get(self, request, *args, **kwargs):
        subscription = request.GET.get('subscription')
        if subscription:
            pk = int(request.GET['project'])
            project = get_object_or_404(models.Project, pk=pk)
            if subscription == 'follow':
                project.project_followers.add(request.user)
                project.save()

            if subscription == 'unfollow':
                project.project_followers.remove(request.user)
                project.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context


class ProjectDetail(LoginRequiredMixin, generic.DetailView):
    """
    Display  a single published project
    """
    model = models.Project
    template_name = 'dashboard/projects/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        
        # Change unseen notification to seen
        unseen_notifications = self.request.user.received_notifications.filter(
            is_seen=False
        ).filter(notification__project=self.object)
        for notification in unseen_notifications:
            notification.is_seen = True
            notification.save()

        context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context


class ProjectCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    """
    Create a new project record
    """
    form_class = forms.ProjectForm
    model = models.Project
    template_name = 'dashboard/projects/project_form.html'
    success_message = 'New project created successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.has_perms('dashboard.admin_project')

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context


class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    Update an existing project record
    """
    form_class = forms.ProjectForm
    model = models.Project
    template_name = 'dashboard/projects/project_form.html'
    success_message = 'Project updated successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.has_perms('dashboard.admin_project')

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'Projects'
        return context
