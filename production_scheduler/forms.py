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
    CORRIGIENDO = 7
    STATUS_CHOICES = (
    (CUTTING, 'Cortando'),
    (ARMANDO, 'Armando'),
    (TERMINADA, 'Terminada'),
    (CORRIGIENDO, 'Corrigiendo')
    )
    status = forms.ChoiceField( label=False, choices=STATUS_CHOICES)

class LineItemEntregadaForm(forms.Form):
    #Choices
    TERMINADA = 4
    ENTREGADA = 5
    ERROR = 6
    STATUS_CHOICES = (
    (TERMINADA, 'Terminada'),
    (ENTREGADA, 'Entregada'),
    (ERROR, 'Corregir Error')
    )
    status = forms.ChoiceField( label=False, choices=STATUS_CHOICES)

class LineItemSpecialInstructionsForm(forms.Form):
    nota = forms.CharField()
