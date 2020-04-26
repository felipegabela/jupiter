from django.db import models
from django.conf import settings
from production_scheduler.models import LineItem

class Log(models.Model):
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    event_body = models.TextField()
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    is_event = models.BooleanField()

class InboxReadControl(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    last_event_viewed_date = models.DateTimeField()
