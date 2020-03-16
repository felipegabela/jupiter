from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'production_scheduler'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('assign_order/', views.assign_order, name='assign_order'),
]
