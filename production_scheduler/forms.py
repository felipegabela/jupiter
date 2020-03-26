from django import forms
from django.shortcuts import render
from .models import Seamstress, LineItem

class SeamstressListForm(forms.Form):
    seamstress_id = forms.ChoiceField( label=False,
        choices=[(seamstress.seamstress_id, seamstress.alias) for seamstress in Seamstress.objects.all()])

class StatusForm(forms.Form):
    #Choices
    CUTTING = 2
    ARMANDO = 3
    TERMINADA = 4
    STATUS_CHOICES = (
    (CUTTING, 'Cortando'),
    (ARMANDO, 'Armando'),
    (TERMINADA, 'Terminada')
    )
    status = forms.ChoiceField( label=False, choices=STATUS_CHOICES)
