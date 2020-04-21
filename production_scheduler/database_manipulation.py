from .models import LineItem, Seamstress
from .models import Product, Message
from django.db.models import Exists
import datetime

# Retrieve all line items in progresss assigned to a seamstress from database
# Used in: new_orders_view > NewOrdersView > get > Seamstress View
def retrieve_orders_in_progress_assigned_to_seamstress__(seamstress_id):
    line_items = LineItem.objects.filter(assigned_to=seamstress_id).order_by('order_number')
    line_items_list = []
    for item in line_items:
        if item.status != 5:
            line_items_list.append(item)
    return line_items_list

# Update line item status
# Response codes:
# -1 = line item doesn't exist
#  0 = line item is not assigned, can't change it to other status
#  1 = line item status changed
#  2 = invalid status code
#  3 = fatal eror
def update_line_item_status__(line_item_id, status):
    current_status = LineItem.objects.filter(line_item_id=line_item_id)[0].status
    #Check if line item exists
    ls_len = len(list(LineItem.objects.filter(line_item_id=line_item_id)))
    if ls_len != 1:
        return -1

    # Change status to assigned
    if status == '1':
        #Check if line item is assigned before changing the status
        ls_len = len(list(LineItem.objects.filter(line_item_id=line_item_id, assigned_to__isnull=False)))
        if ls_len == 0:
            return 0

        to_update = LineItem.objects.filter(line_item_id=line_item_id).update(status=status)
        return 1
    # Change status to any other status except 'new'
    elif (status == '2' or status == '3' or status == '4' or
            status == '5' or status == '6' or status == '7'):
        # Line item status change from Terminado -> Entregada
        if current_status == 4 and int(status) == 5:
            to_update = LineItem.objects.filter(line_item_id=line_item_id).update(fecha_entrega=datetime.date.today())
        # Line item status change from Entregada -> Terminado
        if current_status == 5 and int(status) == 4:
            to_update = LineItem.objects.filter(line_item_id=line_item_id).update(fecha_entrega=None)

        to_update = LineItem.objects.filter(line_item_id=line_item_id).update(status=status)
        return 1
    # Invalid status code
    else:
        return 2

    return 3

# Update line item special instructions
def update_line_time_special_instructions__(line_item_id, nota):
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(special_instructions=nota)

# Update line item assignment date
def update_line_item_assignment_date(line_item_id, currentDate):
    if currentDate == True:
        to_update = LineItem.objects.filter(line_item_id=line_item_id).update(fecha_assignacion=datetime.date.today())

# Assign line item to seamstress
# Response codes:
# -2 = seamstress doesn't exist
# -1 = line item doesn't exist
#  1 = line item asigned to seamstress
def assign_line_item_to_seamstress__(line_item_id, seamstress_id):
    #Check if seamstress exists
    ls_len = len(list(Seamstress.objects.filter(seamstress_id=seamstress_id)))
    if ls_len != 1:
        return -2
    #Check if line item exists
    ls_len = len(list(LineItem.objects.filter(line_item_id=line_item_id)))
    if ls_len != 1:
        return -1
    # If the seamstress and the line item exists, proceed
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(assigned_to=seamstress_id)
    return 1

# Retrieve line items from database by status
def retrieve_orders_by_status__(status):
    line_items = LineItem.objects.filter(status=status).order_by('order_number')
    line_items_list = [item for item in line_items]
    return line_items_list

# Retrieve all line items assigned to a seamstress from database
def retrieve_all_orders_assigned_to_seamstress__(seamstress_id):
    line_items = LineItem.objects.filter(assigned_to=seamstress_id).order_by('order_number')
    line_items_list = [item for item in line_items]
    return line_items_list




#Retrieve orders from database by status and seamstress
def retrieve_orders_by_status_seamstress__(status, seamstress):
    line_items = LineItem.objects.filter(status=status, assigned_to=seamstress)
    line_items_list = [item for item in line_items]
    return line_items_list

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

#Save new line items to database
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

#Retrieve messages from database assigned to and especific line_item
def retrieve_messages_by_line_item__(line_item_id):
    messages = Message.objects.filter(line_item_id=line_item_id)
    messages_list = [item for item in messages]
    return messages_list
