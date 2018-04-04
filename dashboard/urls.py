from django.urls import path, include
from .views import projects, users


app_name = 'dashboard'


urlpatterns = [
    # Signup/Register
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', users.signup, name='register'),

    # Projects
    path('', projects.index, name='index'),
    path('projects/', projects.ProjectList.as_view(), name='project-list'),
    path('project/<int:pk>', projects.ProjectDetail.as_view(), name='project-detail'),
    path('project/create/', projects.ProjectCreate.as_view(), name='project-create'),
]
