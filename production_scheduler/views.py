from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

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

    #Shopify Order API Production
    #url = 'https://@remu-apparel.myshopify.com/admin/api/2020-01/orders.json?'
    #user = '524bbdf763023b8fa2382d180c736a41'
    #password = 'c9f2098976af4b1868a34bb4add02f4e'

    #Shopify Order API Testing
    url = 'https://@remu-international.myshopify.com/admin/api/2020-01/orders.json?'
    user = '6e4440f817fb00deef93767c52f24830'
    password = 'c2bf6e5be194d46e2d8b7b6b3b137a4f'

    #GET API call
    query_params={
        'fields': 'order_number, id, created_at, fulfillment_status, customer, line_items',
        'limit': '30', 'status': 'any'} #status = any, fulfilled, ''
    try:
        response = requests.get(
            url, params = query_params, verify = True, timeout = 5,
            auth=HTTPBasicAuth(user, password))

    except Timeout as e:
        timeout = True
        #print(e)
    except ConnectionError as e:
        connection_error = True
        #print(e)
    except requests.exceptions.RequestException as e:
        http_error = True
        #print(e)

    else:
        #Checking response status
        response_status = response.status_code
        if response_status == 200:
            response_body = response.json()
            orders = response_body['orders']
        else:
            response_body = 'An error has occured. Error code ' + str(response_status)

    context = {
        'orders': orders,'http_status': response_status,
        'timeout': timeout, 'connection_error': connection_error, 'http_error' : http_error
        }
    return render(request, 'production_scheduler/home.html', context)
