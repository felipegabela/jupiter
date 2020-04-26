from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from production_scheduler.models import LineItem
from .models import Log
from .db_manipulation import *
from .forms import *
from users.models import CustomUser

@login_required()
def view_log(request, line_item_id):
    template_name = 'log/log.html'
    form = LogForm
    user_id = request.user.id
    log = retrieve_line_item_log__(line_item_id, user_id)
    context = {
                'line_item_id':line_item_id,
                'form':form,
                'log':log
            }
    return render(request, template_name, context)

@login_required()
def add_log_message(request):
    if (request.method == "POST"):
        event_body = request.POST['event_body']
        line_item_id = request.POST['line_item_id']
        log = Log(
                    line_item_id= LineItem.objects.get(pk=line_item_id),
                    event_body = event_body,
                    username=CustomUser.objects.get(pk=request.user.id),
                    is_event = False
                )
        log.save()
        return redirect('log:view_log', line_item_id=line_item_id)
    raise(Http404)
