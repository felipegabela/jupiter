from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from .models import LineItem
from .models import Product

import urllib.parse
import requests

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):
    #Default initialization of context params.
    response_status = None
    timeout = False
    connection_error = False
    http_error = False
    orders = []

    #Shopify Order API Testing
    url = 'https://@remu-international.myshopify.com/admin/api/2020-01/orders.json?'
    user = '6e4440f817fb00deef93767c52f24830'
    password = 'c2bf6e5be194d46e2d8b7b6b3b137a4f'

    #GET API call
    query_params={
        'fields': 'order_number, id, created_at, fulfillment_status, line_items',
        'limit': '50', 'status': 'any'} #status = any, fulfilled, ''
    try:
        response = requests.get(
            url, params = query_params, verify = True, timeout = 5,
            auth=HTTPBasicAuth(user, password))

    except Timeout as e:
        timeout = True
        print(e)
    except ConnectionError as e:
        connection_error = True
        print(e)
    except requests.exceptions.RequestException as e:
        http_error = True
        print(e)

    else:
        #Checking response status
        response_status = response.status_code
        if response_status == 200:
            response_body = response.json()
            orders = response_body['orders']
        else:
            response_body = 'An error has occured. Error code ' + str(response_status)

    #Save new orders to database
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

    #Retrieve unassigened others from data base
    line_items = LineItem.objects.filter(status=0)
    line_items_list = [item for item in line_items]

    context = {
        'line_items_list': line_items_list,'http_status': response_status,
        'timeout': timeout, 'connection_error': connection_error, 'http_error' : http_error
        }
    return render(request, 'production_scheduler/home.html', context)
