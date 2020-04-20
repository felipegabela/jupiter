from .models import LineItem
from .models import Product, Message
from django.db.models import Exists
import datetime

#Assign order to seamstress
def assign_line_item_to_seamstress__(line_item_id, seamstress_id):
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(assigned_to=seamstress_id)

#Update line item status
def update_line_item_status__(line_item_id, status):
    ls_len = len(list(LineItem.objects.filter(line_item_id=line_item_id, assigned_to__isnull=False)))
    if ls_len == 0:
            return False
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(status=status)
    return True

#Update line item special instructions
def update_line_time_special_instructions__(line_item_id, nota):
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(special_instructions=nota)

#Update line item assignment Date
def update_line_item_assignment_date(line_item_id, currentDate):
    if currentDate == True:
        to_update = LineItem.objects.filter(line_item_id=line_item_id).update(fecha_assignacion=datetime.date.today())
#Retrieve line items from database by status
def retrieve_orders_by_status__(status):
    line_items = LineItem.objects.filter(status=status).order_by('order_number')
    line_items_list = [item for item in line_items]
    return line_items_list

#Retrieve orders from database by status and seamstress
def retrieve_orders_by_status_seamstress__(status, seamstress):
    line_items = LineItem.objects.filter(status=status, assigned_to=seamstress)
    line_items_list = [item for item in line_items]
    return line_items_list

#Retrieve messages from database assigned to and especific line_item
def retrieve_messages_by_line_item__(line_item_id):
    messages = Message.objects.filter(line_item_id=line_item_id)
    messages_list = [item for item in messages]
    return messages_list

#Retrieve all current line items in production from data base
def retrieve_orders_in_production_by_seamstress__(seamstress):
    if seamstress != None:
        line_items_1= LineItem.objects.filter(status=1, assigned_to=seamstress)
        line_items_2 = LineItem.objects.filter(status=2, assigned_to=seamstress)
        line_items_3 = LineItem.objects.filter(status=3, assigned_to=seamstress)
    else:
        line_items_1= LineItem.objects.filter(status=1)
        line_items_2 = LineItem.objects.filter(status=2)
        line_items_3 = LineItem.objects.filter(status=3)

    line_items = line_items_1.union(line_items_2, line_items_3).order_by('order_number')
    line_items_list = [item for item in line_items]
    return line_items_list

#Retrieve all line items assigned to a seamstress from database
def retrieve_orders_assigned_to_seamstress__(seamstress_id):
    line_items = LineItem.objects.filter(assigned_to=seamstress_id).order_by('order_number')
    line_items_list = [item for item in line_items]
    return line_items_list

#Retrieve all line items in progresss assigned to a seamstress from database
def retrieve_orders_in_progress_assigned_to_seamstress__(seamstress_id):
    line_items = LineItem.objects.filter(assigned_to=seamstress_id).order_by('order_number')
    line_items_list = []
    for item in line_items:
        if item.status != 5:
            line_items_list.append(item)
    return line_items_list

#Save new orders to database
def save_new_orders(orders):
    for order in orders:
       for item in order['line_items']:
           #Checking if item has not been fulfilled yet
           if order['fulfillment_status'] is None:
               #Checking that product is not already in the database
               if not LineItem.objects.filter(line_item_id=item['id']).exists():
                   product = Product.objects.get(product_sku=item['sku'])
                   nombre_producto = product.nombre_producto
                   split = nombre_producto.split(";")
                   product_title= split[0]
                   product_variant_title= split[1]

                   #Transforming Date
                   datetime = order['created_at']
                   tmp = datetime.split("T")
                   date = tmp[0]

                   new_line_item = LineItem(
                       line_item_id=item['id'], title=product_title, quantity=item['quantity'],
                       product_sku=item['sku'], variant_title=product_variant_title,
                       order_id=order['id'], order_number=order['order_number'],
                       created_at=date, status=0)
                   new_line_item.save()
