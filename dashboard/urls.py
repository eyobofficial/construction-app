from django.urls import path
from .views import projects


app_name = 'dashboard'


urlpatterns = [
    
    # Projects
    path('projects/', projects.ProjectList.as_view(), name='project-list'),
]
