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
from .database_manipulation import *
from .forms import AssignForm, StatusForm

@login_required()
def historial(request):
    template_name = None
    #Historial Seamstress View
    if request.user.groups.filter(name='seamstress').exists():
        template_name='production_scheduler/historial.html'
        #Retrieve new others from data base
        user_id = request.user.id
        seamstress_id = Seamstress.objects.get(username=user_id).seamstress_id
        line_items_list = retrieve_orders_assigned_to_seamstress__(seamstress_id)
        context = {
            'line_items_list': line_items_list,
            }
        return render(request, template_name, context)
    else:
        return redirect('production_scheduler:home')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        template_name, context= [None] * 2

        #Seamstress Home View (New Orders)
        if self.request.user.groups.filter(name='seamstress').exists():
            template_name='production_scheduler/mis-ordenes.html'
            form = StatusForm
            #Retrieve new others from data base
            user_id = self.request.user.id
            seamstress_id = Seamstress.objects.get(username=user_id).seamstress_id
            line_items_list = retrieve_orders_in_progress_assigned_to_seamstress__(seamstress_id)
            context = {
                'line_items_list': line_items_list, 'form': form,
                }

        #Coordinator Home View (New Orders)
        if self.request.user.groups.filter(name='coordinator').exists():
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
            line_items_list = retrieve_orders_by_status__(0) #NEW = 0

            context = {
                'line_items_list': line_items_list,'http_status': response_status,
                'timeout': timeout, 'connection_error': connection_error,
                'http_error' : http_error, 'form' : form,
                }

        return render(request, template_name, context)


@login_required()
def assign_line_item_to_seamstress(request):
    if request.is_ajax() and 'assign_line_item_to_seamstress' in request.POST and request.method == "POST" :
        seamstress_id = request.POST['assign']
        line_item_id = request.POST['line_item_id']
        assign_line_item_to_seamstress__(line_item_id, seamstress_id)
        data = {
            'message': "Assigment Successful.",
            'line_item_id': line_item_id,
            'assigned_to': Seamstress.objects.get(seamstress_id=seamstress_id).alias
        }
        return JsonResponse(data)
    else:
        return redirect('production_scheduler:home')


@login_required()
def change_line_item_status(request):
    if 'change_line_item_status' in request.POST and request.method == "POST":
        line_item_id = request.POST['line_item_id']
        update_line_item_status__(line_item_id, 1) # Assigned = 1
    return redirect('production_scheduler:home')

@login_required()
def update_line_item_status(request):
    if request.is_ajax() and 'update_line_item_status' in request.POST and request.method == "POST" :
        status = request.POST['status']
        line_item_id = request.POST['line_item_id']
        update_line_item_status__(line_item_id, status)
        status_display_name = LineItem.objects.get(line_item_id=line_item_id).get_status_display()
        data = {
            'message': "Successfully Updated Status.",
            'line_item_id': line_item_id,
            'new_status': status_display_name
        }
        return JsonResponse(data)
    else:
        return redirect('production_scheduler:home')
