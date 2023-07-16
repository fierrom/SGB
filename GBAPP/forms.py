from django import forms
from django.utils import timezone

class SearchForm(forms.Form):
    query = forms.CharField(label='Busqueda', required=True)

class Calendar(forms.Form):
    my_datetime = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}), input_formats=['%d/%m/%Y', '%d/%m/%y'])
