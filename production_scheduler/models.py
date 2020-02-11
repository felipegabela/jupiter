from django.db import models
from django.conf import settings

class Product(models.Model):
    product_sku = models.CharField(max_length=25, primary_key=True)
    product_name = models.CharField(max_length=100)
    nombre_producto = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name


class Seamstress(models.Model):
    seamstress_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workshop = models.CharField(max_length=50)
    seamstress_name = models.CharField(max_length=50)
    seamstress_lastname = models.CharField(max_length=50)

    def __str__(self):
        return self.seamstress_name


class LineItem(models.Model):
    line_item_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_sku = models.CharField(max_length=25)
    properties = models.BooleanField()
    variant_title = models.CharField(max_length=100)
    order_id = models.CharField(max_length=20)
    order_number = models.CharField(max_length=20)
    created_at = models.DateField()
    assigned_to = models.CharField(max_length=25)
    #Choices
    NEW = 0
    ASSIGNED = 1
    CUTTING = 2
    OJALES = 3
    READY = 4
    STATUS_CHOICES = (
    (NEW, 'New'),
    (ASSIGNED, 'Assigned'),
    (CUTTING, 'Cutting'),
    (OJALES, 'Ojales'),
    (READY, 'Ready')
    )
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

class Propiedades(models.Model):
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value

class Message(models.Model):
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    message_body = models.TextField()
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    publication_date = models.DateTimeField()
