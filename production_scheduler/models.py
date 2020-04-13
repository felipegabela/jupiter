from django.db import models
from django.conf import settings

class Product(models.Model):
    product_sku = models.CharField(max_length=25, primary_key=True)
    product_name = models.CharField(max_length=200)
    nombre_producto = models.CharField(max_length=200)

    def __str__(self):
        return self.product_name


class Seamstress(models.Model):
    seamstress_id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=100, blank=True, null=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.alias

class LineItem(models.Model):
    line_item_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_sku = models.CharField(max_length=25)
    variant_title = models.CharField(max_length=100)
    order_id = models.CharField(max_length=20)
    order_number = models.CharField(max_length=20)
    created_at = models.DateField()
    assigned_to = models.ForeignKey(Seamstress, on_delete=models.SET_NULL, blank=True, null=True)
    special_instructions = models.CharField(max_length=300, blank=True, null=True)
    #Choices
    NEW = 0
    ASSIGNED = 1
    CUTTING = 2
    ARMANDO = 3
    TERMINADA = 4
    ENTREGADA = 5
    ERROR = 6
    CORRIGIENDO = 7
    STATUS_CHOICES = (
    (NEW, 'Nueva'),
    (ASSIGNED, 'Asignada'),
    (CUTTING, 'Cortando'),
    (ARMANDO, 'Armando'),
    (TERMINADA, 'Terminada'),
    (ENTREGADA, 'Entregada'),
    (ERROR, 'Corregir Error'),
    (CORRIGIENDO, 'Corrigiendo')
    )
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    fecha_entrega = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    message_body = models.TextField()
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateTimeField(auto_now_add=True)
