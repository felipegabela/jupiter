from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import TemplateView

from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from .models import LineItem
from .models import Product
from .utilities import save_new_orders
from .forms import AssignForm

import urllib.parse
import requests

class HomeView(TemplateView):
    template_name='production_scheduler/home.html'

    def get(self, request):
        #Default initialization of context params.
        response_status = None
        timeout = False
        connection_error = False
        http_error = False
        orders = []
        assign_form = AssignForm()

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

        #Error Handling
        except Timeout as e:
            timeout = True
            print(e)
        except ConnectionError as e:
            connection_error = True
            print(e)
        except requests.exceptions.RequestException as e:
            http_error = True
            print(e)

        #Succesfull API call
        else:
            #Checking response status
            response_status = response.status_code
            if response_status == 200:
                response_body = response.json()
                orders = response_body['orders']
            #HTTP Error
            else:
                response_body = 'An error has occured. Error code ' + str(response_status)

        #Save new orders to database
        save_new_orders(orders)

        #Retrieve new others from data base
        line_items = LineItem.objects.filter(status=0)
        line_items_list = [item for item in line_items]

        #Prepare Context
        context = {
            'line_items_list': line_items_list,'http_status': response_status, 'assign_form': assign_form,
            'timeout': timeout, 'connection_error': connection_error, 'http_error' : http_error
            }

        return render(request, self.template_name, context)
