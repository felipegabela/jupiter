from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Seamstress
from .database_manipulation import *
from .forms import *

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
