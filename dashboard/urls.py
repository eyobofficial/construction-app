from django.urls import path
from .views import projects


app_name = 'dashboard'


urlpatterns = [
    # Projects
    path('projects/', projects.ProjectList.as_view(), name='project-list'),
    path('project/<int:pk>', projects.ProjectDetail.as_view(), name='project-detail'),
    path('project/create/', projects.ProjectCreate.as_view(), name='project-create'),
]
