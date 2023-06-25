from datetime import datetime
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *


@login_required()
def login_success(request):
    return render(request, 'GBAPP/index2.html')

@login_required()
def vinedo_list(request):
    """Listado de vinedo"""
    vin = vinedo.objects.all()
    vin_status = Estadovinedo.objects.all()
    context = {
            "vinedo_list": vin,
            "vinedo_status_list": vin_status,
        }
    return render(request, 'GBAPP/vinedo_list.html', context)

@login_required()
def vinedo_detail(request, vinedo_id):
    vin = get_object_or_404(vinedo, pk=vinedo_id)
    estvin = Estadovinedo.objects.all()
    context = {
        "vinedo": vin,
        "estvine" : estvin
    }
    return render(request, 'GBAPP/vinedo_detail.html', context)

@login_required()
def vinedo_update(request, vinedo_id):
    vin = get_object_or_404(vinedo, pk=vinedo_id)
    new_name = request.POST.get('name',False)
    new_ubic = request.POST.get('ubic',False)
    new_dueno = request.POST.get('dueno',False)
    new_status = request.POST.get('status',False)
    vin.Nombre = new_name
    vin.Estado = Estadovinedo(id=new_status)
    vin.Ubicacion = new_ubic
    vin.Dueno = new_dueno
    vin.save()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def new_vinedo_form(request):
    lastnumvin = vinedo.objects.filter().values_list('NumeroVin', flat=True).last()
    Numvin = lastnumvin + 1
    cre_date = datetime.today()
    estvin = Estadovinedo.objects.all()
    context = {
        "NumVin": Numvin,
        "credate": cre_date,
        "estvine": estvin
    }
    if request.method == 'POST':
        vin = vinedo()
        new_name = request.POST.get('name',False)
        new_ubic = request.POST.get('ubic', False)
        new_dueno = request.POST.get('dueno',False)
        new_status = request.POST.get('status', False)
        vin.NumeroVin = Numvin
        vin.Nombre = new_name
        vin.Estado = Estadovinedo(id=new_status)
        vin.created_date = cre_date
        vin.Ubicacion = new_ubic
        vin.Dueno = new_dueno
        vin.save()
        return HttpResponseRedirect(reverse('vinedo_list'))
    return render(request, 'GBAPP/new_vinedo_form.html', context)

@login_required()
def detele_vinedo(request, vinedo_id):
    vin = get_object_or_404(vinedo, pk=vinedo_id)
    vin.delete()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def pesada_detail(request, pesada_id):
    pesada = get_object_or_404(Pesada, pk=pesada_id)
    camionero = Camionero.objects.filter(Estado__Estado='Activo')
    variet = Varietal.objects.all()
    vin = vinedo.objects.filter(Estado__Estado='Activo')
    context = {
        "pesada_list": pesada,
        "camionero_list": camionero,
        "varietal": variet,
        "vinedo": vin,
    }
    return render(request, 'GBAPP/pesada_detail.html', context)

@login_required()
def pesada_update(request, pesada_id):
    pes = get_object_or_404(Pesada, pk=pesada_id)
    new_varie = request.POST.get('varie', False)
    new_camio = request.POST.get('camion', False)
    new_vine = request.POST.get('vine', False)
    new_tara = request.POST.get('Tara', False)
    new_bruto = request.POST.get('PesoBruto', False)
    new_pesnet = int(new_bruto) - int(new_tara)
    pes.Vinedo_id = int(new_vine)
    pes.Tara = new_tara
    pes.PesoNeto = new_pesnet
    pes.PesoBruto = new_bruto
    pes.Camionero = Camionero(id=new_camio)
    pes.Varietal = Varietal(id=new_varie)
    pes.save()
    return HttpResponseRedirect(reverse('pesada_list'))

@login_required()
def pesada_list(request):
    pesada = Pesada.objects.filter(Eliminado="0")
    context = {
        "pesada_list": pesada,
    }
    return render(request, 'GBAPP/pesada_list.html', context)

def search_view(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Pesada.objects.filter(Vinedo__Nombre__icontains=query)

    return render(request, 'GBAPP/buscar_pesada.html', {'form': form, 'results': results})

@login_required()
def new_pesada_form(request):
    lastnumpes = Pesada.objects.filter().values_list('NumeroPesada', flat=True).last()
    NumPes = lastnumpes + 1
    cre_date = datetime.today()
    camio = Camionero.objects.filter(Estado__Estado='Activo')
    variet = Varietal.objects.all()
    vin = vinedo.objects.filter(Estado__Estado='Activo')
    context = {
        "NumPes": NumPes,
        "credate": cre_date,
        "varietal": variet,
        "camionero": camio,
        "vin": vin,
    }
    if request.method == 'POST':
        pes = Pesada()
        new_varie = request.POST.get('varie', False)
        new_camio = request.POST.get('camion', False)
        new_vine = request.POST.get('vine', False)
        new_tara = request.POST.get('Tara', False)
        new_bruto = request.POST.get('PesoBruto', False)
        new_pesnet = int(new_bruto) - int(new_tara)
        pes.Vinedo_id = int(new_vine)
        pes.Tara = new_tara
        pes.PesoNeto = new_pesnet
        pes.PesoBruto = new_bruto
        pes.created_date = cre_date
        pes.Camionero = Camionero(id=new_camio)
        pes.Varietal = Varietal(id=new_varie)
        pes.save()
        return HttpResponseRedirect(reverse('pesada_list'))
    return render(request, 'GBAPP/new_pesada_form.html', context)