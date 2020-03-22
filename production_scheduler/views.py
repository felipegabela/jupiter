import urllib.parse
import requests

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.urls import reverse
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

from .models import LineItem
from .models import Product
from .models import Seamstress
from .utilities import save_new_orders, retrieve_new_orders
from .forms import AssignForm

#from django.conf import settings
#from django.http import Http404
#from django.contrib.auth import logout
#from django.views.decorators.cache import cache_control, never_cache
#from django.http import HttpResponseRedirect, HttpResponse
#from django.shortcuts import get_object_or_404

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        template_name='production_scheduler/home.html'
        response_status = None
        timeout, connection_error, http_error = [False] * 3
        orders = []
        form = AssignForm

        #Shopify Order API
        url = 'https://@remu-international.myshopify.com/admin/api/2020-01/orders.json?'
        user = '6e4440f817fb00deef93767c52f24830'
        password = 'c2bf6e5be194d46e2d8b7b6b3b137a4f'
        #GET API call
        query_params={
            'fields': 'order_number, id, created_at, fulfillment_status, line_items',
            'limit': '50', 'status': 'any' # or fulfilled
            }
        try:
            response = requests.get(
                url, params = query_params, verify = True, timeout = 5,
                auth=HTTPBasicAuth(user, password)
                )
        #Error Handling
        except Timeout as e:
            timeout = True
        except ConnectionError as e:
            connection_error = True
        except requests.exceptions.RequestException as e:
            http_error = True

        #Succesfull API call
        else:
            response_status = response.status_code
            if response_status == 200:
                response_body = response.json()
                orders = response_body['orders']
            else:
                response_body = 'An error has occured. HTTP response code ' + str(response_status)

        #Save new orders to database
        save_new_orders(orders)
        #Retrieve new others from data base
        line_items_list = retrieve_new_orders()

        context = {
            'line_items_list': line_items_list,'http_status': response_status,
            'timeout': timeout, 'connection_error': connection_error,
            'http_error' : http_error, 'form' : form,
            }

        return render(request, template_name, context)


@login_required()
def assign_line_item_to_seamstress(request):
    if request.is_ajax() and 'assign_line_item_to_seamstress' in request.POST and request.method == "POST" :
        assign_input = request.POST['assign']
        line_item_id = request.POST['line_item_id']
        to_update = LineItem.objects.filter(line_item_id=line_item_id).update(assigned_to=assign_input)
        new_assignment = Seamstress.objects.filter(seamstress_id=assign_input)
        data = {
            'message': "Assigment Successful.",
            'line_item_id': line_item_id,
            'new_assigment': new_assignment[0].alias
        }
        return JsonResponse(data)
    else:
        return redirect('production_scheduler:home')


@login_required()
def change_line_item_status(request):
    if 'change_line_item_status' in request.POST and request.method == "POST":
        line_item_id = request.POST['line_item_id']
        to_update = LineItem.objects.filter(line_item_id=line_item_id).update(status=1) #ASSIGNED = 1
    return redirect('production_scheduler:home')
