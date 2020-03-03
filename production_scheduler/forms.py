from django import forms
from .models import Seamstress

class AssignForm(forms.Form):
    assign = forms.ChoiceField( label=False, 
        choices=[(seamstress.seamstress_id, seamstress.alias) for seamstress in Seamstress.objects.all()])
