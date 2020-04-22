from django.contrib import admin
from .models import LineItem, Seamstress, Product
from .models import Log, InboxReadControl

admin.site.register(Product)
admin.site.register(Seamstress)
admin.site.register(LineItem)
admin.site.register(Log)
admin.site.register(InboxReadControl)
