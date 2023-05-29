"""import mimetypes
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
import hashlib
"""
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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