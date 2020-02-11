from django.urls import path

from . import views

app_name = 'production_scheduler'
urlpatterns = [
    path('', views.home, name='production_scheduler-home'),
]
