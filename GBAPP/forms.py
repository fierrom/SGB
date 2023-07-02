from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Busqueda', required=True)

class Calendar(forms.Form):
    my_date = forms.DateField(widget=forms.SelectDateWidget,label="Elije Fecha")