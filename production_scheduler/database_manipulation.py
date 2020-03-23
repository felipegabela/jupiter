from .models import LineItem
from .models import Product

#Assign order to seamstress
def assign_line_item_to_seamstress__(line_item_id, seamstress_id):
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(assigned_to=seamstress_id)

#Update line item status
def update_line_item_status__(line_item_id, status):
    to_update = LineItem.objects.filter(line_item_id=line_item_id).update(status=status)

#Retrieve orders from database by status
def retrieve_orders_by_status__(status):
    line_items = LineItem.objects.filter(status=status)
    line_items_list = [item for item in line_items]
    return line_items_list

#Retrieve all orders assigned to a seamstress from database
def retrieve_orders_assigned_to_seamstress__(seamstress_id):
    line_items = LineItem.objects.filter(assigned_to=seamstress_id)
    line_items_list = [item for item in line_items]
    return line_items_list

#Retrieve all orders in progresss assigned to a seamstress from database
def retrieve_orders_in_progress_assigned_to_seamstress__(seamstress_id):
    line_items = LineItem.objects.filter(assigned_to=seamstress_id)
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
                       product_sku=item['sku'], properties=False, variant_title=product_variant_title,
                       order_id=order['id'], order_number=order['order_number'],
                       created_at=date, status=0)
                   new_line_item.save()