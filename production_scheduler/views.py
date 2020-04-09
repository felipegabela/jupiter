import urllib.parse
import requests
import numbers
import os

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.urls import reverse
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError

from .models import LineItem, Message
from .models import Product
from .models import Seamstress
from .database_manipulation import *
from .forms import *
from users.models import CustomUser

@login_required()
def mensajes(request, line_item_id):
    template_name = 'production_scheduler/mensajes.html'
    form = MessageForm
    mensajes = retrieve_messages_by_line_item__(line_item_id)
    context = {
                'line_item_id':line_item_id,
                'form':form,
                'mensajes':mensajes
            }
    return render(request, template_name, context)

@login_required()
def historial(request, option, filter):
    template_name = None

    #Historial Seamstress View
    if (request.user.groups.filter(name='seamstress').exists()
            and option == 'costurera') :
        template_name='production_scheduler/historial.html'
        #Retrieve all line items assigned to seamstress from data base
        user_id = request.user.id
        seamstress_id = Seamstress.objects.get(username=user_id).seamstress_id
        line_items_list = retrieve_orders_assigned_to_seamstress__(seamstress_id)
        context = {
            'line_items_list': line_items_list,
            'option': option,
            }
        return render(request, template_name, context)

    #Lista chaquetas en produccion: Coodinator View
    elif (request.user.groups.filter(name='coordinator').exists()
            and option == 'produccion') :
        template_name='production_scheduler/historial.html'
        seamstressListForm = SeamstressListForm
        #Retrieve all current line items in production from data base
        if filter != 'none':
            line_items_list = retrieve_orders_in_production_by_seamstress__(filter)
        else:
            line_items_list = retrieve_orders_in_production_by_seamstress__(None)
        context = {
            'line_items_list': line_items_list,
            'option': option, 'coordinator': True,
            'seamstressListForm': seamstressListForm,
            }
        return render(request, template_name, context)

    #Lista chaquetas terminadas: Coodinator View
    elif (request.user.groups.filter(name='coordinator').exists()
            and option == 'terminadas') :
        template_name='production_scheduler/historial.html'
        seamstressListForm = SeamstressListForm
        lineItemEntregadaForm = LineItemEntregadaForm
        if filter != 'none':
            line_items_list = retrieve_orders_by_status_seamstress__(4, filter) #4 = Terminada
        else:
            line_items_list = retrieve_orders_by_status__(4) #4 = Terminada
        context = {
            'line_items_list': line_items_list,
            'option': option, 'coordinator': True,
            'seamstressListForm': seamstressListForm, 'callback_path': request.path,
            'terminadas': True, 'lineItemEntregadaForm': lineItemEntregadaForm,
            }
        return render(request, template_name, context)

    #Historial chaquetas entregadas: Coodinator View
    elif (request.user.groups.filter(name='coordinator').exists()
            and option == 'entregadas') :
        template_name='production_scheduler/historial.html'
        seamstressListForm = SeamstressListForm
        lineItemEntregadaForm = LineItemEntregadaForm
        if filter != 'none':
            line_items_list = retrieve_orders_by_status_seamstress__(5, filter) #5 = Entregadas
        else:
            line_items_list = retrieve_orders_by_status__(5) #5 = Entregadas
        context = {
            'line_items_list': line_items_list,
            'option': option, 'coordinator': True,
            'seamstressListForm': seamstressListForm,
            'entregadas' : True, 'lineItemEntregadaForm': lineItemEntregadaForm,
            }
        return render(request, template_name, context)
    else:
        return redirect('production_scheduler:new_orders')
#End Historial

class NewOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        template_name, context= [None] * 2

        #Seamstress View
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

        #Coordinator View
        if self.request.user.groups.filter(name='coordinator').exists():
            template_name='production_scheduler/new_orders.html'
            response_status = None
            timeout, connection_error, http_error = [False] * 3
            orders = []
            form = SeamstressListForm
            lineItemSpecialInstructionsForm = LineItemSpecialInstructionsForm

            #Shopify Order API
            url = 'https://@remu-international.myshopify.com/admin/api/2020-01/orders.json?'
            user = os.environ.get('SHOPIFY_API_DEV_USER')
            password = os.environ.get('SHOPIFY_API_DEV_PASS')
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
                'lineItemSpecialInstructionsForm': lineItemSpecialInstructionsForm,
                }

        return render(request, template_name, context)
#End NewOrdersView

#Post method to assign line item to seamstress
@login_required()
def assign_line_item_to_seamstress(request, option):
    #Assign line item to seamstress
    if (request.is_ajax() and 'assign_line_item_to_seamstress' in request.POST
            and request.method == "POST" and option == 'assign'):
        seamstress_id = request.POST['seamstress_id']
        line_item_id = request.POST['line_item_id']
        #try
        assign_line_item_to_seamstress__(line_item_id, seamstress_id)
        data = {
            'message': "Assigment Successful.",
            'line_item_id': line_item_id,
            'assigned_to': Seamstress.objects.get(seamstress_id=seamstress_id).alias
        }
        return JsonResponse(data)
    #Dismiss: change line item status to assigned
    elif ('uptdate_line_item_status_to_assigned' in request.POST
            and request.method == "POST" and option == 'change_status'):
        line_item_id = request.POST['line_item_id']
        nota = request.POST['nota']
        update_line_item_status__(line_item_id, 1) # Assigned = 1
        update_line_time_special_instructions__(line_item_id, nota)
        return redirect('production_scheduler:new_orders')

    else:
        return redirect('production_scheduler:new_orders')

@login_required()
def filter_line_items_by_seamstress(request, callback):
    if (request.method == "POST"):
        if request.POST['action'] == 'filter':
            filter = request.POST['seamstress_id']
        elif request.POST['action'] == 'reset':
            filter = 'none'
        else:
            filter = 'none'
        return redirect('production_scheduler:historial', option=callback, filter=filter)
    raise(Http404)

@login_required()
def send_message(request):
    if (request.method == "POST"):
        message_body = request.POST['message_body']
        line_item_id = request.POST['line_item_id']
        print(request.user.id)
        message = Message(
                    line_item_id= LineItem.objects.get(pk=line_item_id),
                    message_body = message_body,
                    username=CustomUser.objects.get(pk=request.user.id)
                )
        message.save()
        return redirect('production_scheduler:mensajes', line_item_id=line_item_id)
    raise(Http404)

#Post method for line item status update
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
    elif 'update_line_item_status' in request.POST and request.method == "POST":
        option = request.POST['option']
        status = request.POST['status']
        line_item_id = request.POST['line_item_id']
        update_line_item_status__(line_item_id, status)
        return redirect('production_scheduler:historial', option=option, filter='none')

    else:
        return redirect('production_scheduler:new_orders')
