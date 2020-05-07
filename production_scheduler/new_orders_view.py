# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
##
import urllib.parse
import requests
import os
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from django.views.generic import View
from .models import Seamstress
from .db_manipulation import *
from .forms import *
from django.contrib import messages

class NewOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        template_name, context= [None] * 2

        #Seamstress View
        if self.request.user.groups.filter(name='seamstress').exists():
            template_name='production_scheduler/mis-ordenes.html'
            form = StatusForm #2,3,4,7
            #Retrieve new others from data base
            user_id = self.request.user.id
            seamstress_id = Seamstress.objects.get(username=user_id).seamstress_id
            line_items_list, new_activity_ls = retrieve_orders_in_progress_assigned_to_seamstress__(seamstress_id, user_id)
            context = {
                'line_items_list': line_items_list, 'form': form,
                'new_activity_ls': new_activity_ls,
                }

        #Coordinator View
        elif self.request.user.groups.filter(name='coordinator').exists():
            template_name='production_scheduler/new_orders.html'
            response_status = None
            orders = []
            form = SeamstressListForm
            lineItemSpecialInstructionsForm = LineItemSpecialInstructionsForm

            ##
            message = sendgrid.helpers.mail.Mail(
                from_email='gabelafelipe@gmail.com',
                to_emails='felipe@remuapparel.com',
                subject='Sending with Twilio SendGrid is Fun',
                html_content='<strong>and easy to do anywhere, even with Python</strong>')
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            ##




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
                messages.error(request, "Conection timeout. Couldn't retrieve new orders. Please try again later")
            except ConnectionError as e:
                messages.error(request, "Connection Error. Couldn't retrieve new orders.")
            except requests.exceptions.RequestException as e:
                messages.error(request, "An error has occured. Couldn't retrieve new orders.")

            #Succesfull API call
            else:
                response_status = response.status_code
                if response_status == 200:
                    response_body = response.json()
                    orders = response_body['orders']
                    save_new_orders(orders, request)
                else:
                    error = 'HTTP Error ' + str(response_status) + "Couldn't retrieve new orders."
                    messages.error(request, error)

            #Retrieve new others from data base
            line_items_list = retrieve_orders_by_status_cview__(0)

            context = {
                'line_items_list': line_items_list,'http_status': response_status,
                'form' : form,
                'lineItemSpecialInstructionsForm': lineItemSpecialInstructionsForm,
                }
        #No group assigned
        else:
            template_name='production_scheduler/error.html'
            context = {}

        return render(request, template_name, context)
