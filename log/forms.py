from django import forms
from django.shortcuts import render
from .models import Log

class LogForm(forms.ModelForm):
    event_body = forms.CharField(
                label=False,
                widget=forms.Textarea(
                        attrs={
                            'rows':4,
                            'cols':15,
                        }
                    )
                )
    class Meta:
        model = Log
        fields = [
            'event_body'
        ]
