from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *


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
    context = {
        "vinedo": vin,
    }
    return render(request, 'GBAPP/vinedo_detail.html', context)

@login_required()
def vinedo_update(request, vinedo_id):
    vin = get_object_or_404(vinedo, pk=vinedo_id)
    new_name = request.POST['name']
    new_ubic = request.POST['ubic']
    new_dueno = request.POST['dueno']
    vin.Nombre = new_name
    vin.Ubicacion = new_ubic
    vin.Dueno = new_dueno
    vin.save()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def detele_vinedo(request, vinedo_id):
    vin = get_object_or_404(vinedo, pk=vinedo_id)
    vin.delete()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def bascula_detail(request):
    vin = vinedo.objects.all()
    vin_status = Estadovinedo.objects.all()
    context = {
        "vinedo_list": vin,
        "vinedo_status_list": vin_status,
    }
    return render(request, 'GBAPP/bascula_detail.html')

@login_required()
def bascula_update(request, bascula_id):
    vin = get_object_or_404(vinedo, pk=vinedo_id)
    new_name = request.POST['name']
    new_ubic = request.POST['ubic']
    new_dueno = request.POST['dueno']
    vin.Nombre = new_name
    vin.Ubicacion = new_ubic
    vin.Dueno = new_dueno
    vin.save()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def new_vinedo_form(request):
    asset_list = Activo.objects.all()
    risk_status = EstadoRiesgo.objects.all()
    assets = Activo.objects.all()
    documents = Documentacion.objects.all()
    controls = Control.objects.all()
    incidents = Incidente.objects.all()
    users = User.objects.all()

    context = {
        "asset_list": asset_list,
        "risk_status": risk_status,
        "assets_list": assets,
        "documents_list": documents,
        "controls_list": controls,
        "incidents_list": incidents,
        "users": users
    }

    return render(request, 'SGSI/new_risk.html', context)