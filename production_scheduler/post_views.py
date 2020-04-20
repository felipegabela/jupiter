from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import LineItem
from .models import Seamstress
from .database_manipulation import *
from django.contrib import messages

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
    #Confirmar assignacion: change line item status to assigned
    elif ('uptdate_line_item_status_to_assigned' in request.POST
            and request.method == "POST" and option == 'change_status'):
        line_item_id = request.POST['line_item_id']
        nota = request.POST['nota']
        if update_line_item_status__(line_item_id, 1) == False:
            messages.warning(request, "Por favor asignar a alguien primero.")
        else:
            update_line_time_special_instructions__(line_item_id, nota)
            update_line_item_assignment_date(line_item_id, currentDate= True)
            messages.success(request, "Line item assignado exitosamente!")
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
