from django.contrib import admin
from .models import Product
from .models import Seamstress
from .models import LineItem
from .models import Message

admin.site.register(Product)
admin.site.register(Seamstress)
admin.site.register(LineItem)
admin.site.register(Message)
