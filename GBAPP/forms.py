from django import forms
from django.utils import timezone

class SearchForm(forms.Form):
    query = forms.CharField(label='Busqueda', required=True)

class Calendar(forms.Form):
    # my_date = forms.DateTimeField(widget=forms.SelectDateWidget,label="Elije Fecha", initial=timezone.now().date())
    my_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'datepicker'}))
