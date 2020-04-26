from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name = 'log'
urlpatterns = [
    path('view_log/<line_item_id>', views.view_log, name='view_log'),
    path('add_log_message/', views.add_log_message, name='add_log_message'),
]
