import urllib.parse
import requests
import numbers
import os

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import LineItem, Message
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
