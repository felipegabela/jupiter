from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'production_scheduler'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('change_line_item_status/', views.change_line_item_status, name='change_line_item_status'),
    path('assign_line_item_to_seamstress/', views.assign_line_item_to_seamstress, name='assign_line_item_to_seamstress'),
]
