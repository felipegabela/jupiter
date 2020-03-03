from .models import LineItem
from .models import Product

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
