from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import post_views
from . import new_orders_view
from . import historial_view
from . import mensajes_view

app_name = 'production_scheduler'
urlpatterns = [
    path('', new_orders_view.NewOrdersView.as_view(), name='new_orders'),
    path('historial/<option>/<filter>', historial_view.historial, name='historial'),
    path('assign_line_item_to_seamstress/<option>', post_views.assign_line_item_to_seamstress, name='assign_line_item_to_seamstress'),
    path('update_line_item_status/', post_views.update_line_item_status, name='update_line_item_status'),
    path('filter_line_items_by_seamstress/<callback>', post_views.filter_line_items_by_seamstress, name='filter_line_items_by_seamstress'),
    path('mensajes/<line_item_id>', mensajes_view.mensajes, name='mensajes'),
    path('send_message/', mensajes_view.send_message, name='send_message'),
]
