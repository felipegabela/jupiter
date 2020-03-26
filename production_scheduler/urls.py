from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'production_scheduler'
urlpatterns = [
    path('', views.NewOrdersView.as_view(), name='new_orders'),
    path('historial/<option>/<filter>', views.historial, name='historial'),
    path('assign_line_item_to_seamstress/<option>', views.assign_line_item_to_seamstress, name='assign_line_item_to_seamstress'),
    path('update_line_item_status/', views.update_line_item_status, name='update_line_item_status'),
    path('filter_line_items_by_seamstress/<callback>', views.filter_line_items_by_seamstress, name='filter_line_items_by_seamstress'),
]
