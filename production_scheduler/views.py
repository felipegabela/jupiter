import urllib.parse
import requests

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from .models import LineItem
from .models import Product
from .models import Seamstress
from .utilities import save_new_orders, retrieve_new_orders
from .forms import AssignForm

class HomeView(LoginRequiredMixin, FormView):
    template_name='production_scheduler/home.html'
    form_class = AssignForm
    success_url='/'

    def get_context_data(self, **kwargs):
        #Default initialization of context params.
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

        #if self.request.user.groups.filter(name='coordinador').exists():

        return context

    def form_invalid(self, form):
        response = super(HomeView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(HomeView, self).form_valid(form)
        if self.request.is_ajax():
            assign_input = form.cleaned_data['assign']
            line_item_id = self.request.POST['line_item_id']
            to_update = LineItem.objects.filter(line_item_id=line_item_id).update(assigned_to=assign_input)
            new_assignment = Seamstress.objects.filter(seamstress_id=assign_input)
            data = {
                'message': "Assigment Successful.",
                'line_item_id': line_item_id,
                'new_assigment': new_assignment[0].alias
            }
            return JsonResponse(data)
        else:
            return response

#Order Assigment Ajax
@login_required()
def assign_order(request):
    if request.is_ajax():
        form = AssignForm(request.POST)
        if form.is_valid():
            data = {'message' : 'success'}
            assign_input = form.cleaned_data['assign']
            line_item_id = request.POST['line_item_id']
            to_update = LineItem.objects.filter(line_item_id=line_item_id).update(assigned_to=assign_input)
        else:
            data = {'message' : form.errors}
        return HttpResponse(json.dumps(data), content_type='aplication/json')
    else:
        print('Ajax request not working!!!!')
        raise Http404
