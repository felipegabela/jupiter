from django.contrib import admin
from .models import LineItem, Seamstress, Product

admin.site.register(Product)
admin.site.register(Seamstress)
admin.site.register(LineItem)
