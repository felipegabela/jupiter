from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'production_scheduler'
urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='home'),
]
