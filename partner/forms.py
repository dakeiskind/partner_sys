__author__ = 'Administrator'

from django import forms


class PotentialSearchForm(forms.Form):
    zh_name = forms.CharField(required=False)
    en_name = forms.CharField(required=False)
    licence = forms.CharField(required=False)
    contact = forms.CharField(required=False)
    tax = forms.CharField(required=False)
    orgCode = forms.CharField(required=False)
