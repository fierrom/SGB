from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *


@login_required()
def login_success(request):
    return render(request, 'GBAPP/index2.html')

@login_required()
def test(request):
    return render(request, 'GBAPP/test.html')

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
def pesada_detail(request):
    pesada = Pesada.objects.all()
    camionero = Camionero.objects.all()
    context = {
        "pesada_list": pesada,
        "camionero_list": camionero,
    }
    return render(request, 'GBAPP/pesada_detail.html', context)

@login_required()
def pesada_update(request, Pesada_id):
    pesada = get_object_or_404(vinedo, pk=Pesada_id)
    new_name = request.POST['name']
    camionero = get_object_or_404(vinedo, pk=Camionero)
    new_dueno = request.POST['dueno']
    pesada.Nombre = new_name
    pesada.Ubicacion = camionero
    pesada.Dueno = new_dueno
    pesada.save()
    return HttpResponseRedirect(reverse('pesada_list'))

