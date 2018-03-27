from django.urls import path
from .views import projects


app_name = 'dashboard'


urlpatterns = [
    path('', projects.IndexView.as_view(), name='index'),
]
