from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'production_scheduler'
urlpatterns = [
    path('', views.NewOrdersView.as_view(), name='new_orders'),
    path('historial/', views.historial, name='historial'),
    path('uptdate_line_item_status_to_assigned/', views.uptdate_line_item_status_to_assigned, name='uptdate_line_item_status_to_assigned'),
    path('assign_line_item_to_seamstress/', views.assign_line_item_to_seamstress, name='assign_line_item_to_seamstress'),
    path('update_line_item_status/', views.update_line_item_status, name='update_line_item_status'),
]
