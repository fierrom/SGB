from datetime import datetime
from .forms import SearchForm, Calendar
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from io import BytesIO
from xhtml2pdf import pisa
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.db.models import F
from django.db.models import Max

@login_required()
def login_success(request):
    return render(request, 'GBAPP/indexMenu.html')

@login_required()
def indexABM(request):
    return render(request, 'GBAPP/indexABM.html')

@login_required()
def tanqueABM(request):
    return render(request, 'GBAPP/tanqueABM.html')

@login_required()
def bodega(request):
    return render(request, 'GBAPP/bodegaABM.html')

@login_required()
def informepdf(request):
    prod = get_object_or_404(Cuartel, pk=2)
    context  = {
        "prod": prod,
    }

    return render(request, 'GBAPP/informepdf.html', context)

def generar_informe(request):
    with open('./templates/GBAPP/informepdf.html', 'r' , encoding='utf-8') as file:
        prod = get_object_or_404(Cuartel, pk=1)
        context = {
            "prod" : prod,
        }
        html_content = render_to_string('GBAPP/informepdf.html', context=context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
    pdf_file = BytesIO()
    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find('div', attrs={'name': 'informe'})
    new_html = str(div)
    pisa.CreatePDF(BytesIO(new_html.encode('UTF-8')), pdf_file)
    pdf_data = pdf_file.getvalue()
    pdf_file.close()

    response.write(pdf_data)
    return response


@login_required()
def vinedo_list(request):
    vin = vinedo.objects.all()
    vin_status = Estadovinedo.objects.all()
    context = {
            "vinedo_list": vin,
            "vinedo_status_list": vin_status,
        }
    return render(request, 'GBAPP/Lists/vinedo_list.html', context)

@login_required()
def vinedo_detail(request, NumeroVin):
    vin = get_object_or_404(vinedo, pk=NumeroVin)
    estvin = Estadovinedo.objects.all()
    context = {
        "vinedo": vin,
        "estvine" : estvin
    }
    return render(request, 'GBAPP/Details/vinedo_detail.html', context)

@login_required()
def vinedo_update(request, NumeroVin):
    vin = get_object_or_404(vinedo, pk=NumeroVin)
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
    if lastnumvin == None:
        Numvin = 0
    else:
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
    return render(request, 'GBAPP/New/new_vinedo_form.html', context)

@login_required()
def detele_vinedo(request, NumeroVin):
    vin = get_object_or_404(vinedo, pk=NumeroVin)
    cuar = Cuartel.objects.filter(NumVin__NumeroVin=NumeroVin)
    for cua in cuar:
        cua.delete()
    vin.delete()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def pesada_list(request):
    pesada = Cronograma.objects.filter(Eliminado=False).order_by('InicioPrograma')
    context = {
        "pesada_list": pesada,
    }
    return render(request, 'GBAPP/Lists/pesada_list.html', context)

@login_required()
def pesada_detail(request, pesada_id):
    crono = get_object_or_404(Cronograma, pk=pesada_id)
    camionero = Camionero.objects.filter(Estado__Estado='Vigente')
    variet = Varietal.objects.all()
    vin = vinedo.objects.filter(Estado__Estado='Vigente')
    context = {
        "pesada_list": crono,
        "camionero_list": camionero,
        "varietal": variet,
        "vinedo": vin,
    }
    return render(request, 'GBAPP/Details/pesada_detail.html', context)

@login_required()
def pesada_update(request, pesada_id):
    lastnumpes = Pesada.objects.filter().values_list('NumeroPesada', flat=True).last()
    if lastnumpes == None:
        NumPes = 0
    else:
        NumPes = lastnumpes + 1
    pes = get_object_or_404(Cronograma, pk=pesada_id)
    new_tara = request.POST.get('Tara', False)
    new_bruto = request.POST.get('PesoBruto', False)
    new_pesnet = int(new_bruto) - int(new_tara)
    pesa = Pesada()
    pesa.NumeroPesada = NumPes
    pesa.Tara = new_tara
    pesa.PesoNeto = new_pesnet
    pesa.PesoBruto = new_bruto
    pesa.Cuartel_id = int(pes.NumCuar.id)
    pesa.Vinedo_id = int(pes.NumVin.NumeroVin)
    pes.Eliminado = 1
    pes.save()
    if new_pesnet > 0:
        pesa.Eliminado = 0
        pesa.Bascula = 1
    pesa.save()
    return HttpResponseRedirect(reverse('login_success'))

@login_required()
def new_pesada_form(request):
    lastnumpes = Pesada.objects.filter().values_list('NumeroPesada', flat=True).last()
    if lastnumpes == None:
        NumPes = 1
    else:
        NumPes = lastnumpes + 1
    camio = Camionero.objects.filter(Estado__Estado='Vigente')
    vin = vinedo.objects.filter(Estado__Estado='Vigente')
    context = {
        "NumPes": NumPes,
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
        pes.Camionero = Camionero(id=new_camio)
        pes.Varietal = Varietal(id=new_varie)
        pes.save()
        return HttpResponseRedirect(reverse('pesada_list'))
    return render(request, 'GBAPP/New/new_pesada_form.html', context)

def buscarpesada_view(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Pesada.objects.filter(Vinedo__Nombre__icontains=query)

    return render(request, 'GBAPP/Busqueda/buscar_pesada.html', {'form': form, 'results': results})


@login_required()
def buscartanques_view(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Pesada.objects.filter(Vinedo__Nombre__icontains=query)

    return render(request, 'GBAPP/Busqueda/buscar_tanques.html', {'form': form, 'results': results})

@login_required()
def analisis_list(request):
    ana = Analisis.objects.all()
    context = {
            "analisis_list": ana
        }
    return render(request, 'GBAPP/Lists/analisis_list.html', context)

@login_required()
def analisis_tipo_list(request,analisise_id):
    ana = AnalisisE.objects.filter(NumAnali=analisise_id)
    anali = get_object_or_404(Analisis,pk=analisise_id)
    context = {
            "analisis_list": ana,
            "anali" :anali
        }
    return render(request, 'GBAPP/Lists/analisis_tipo_list.html', context)


@login_required()
def new_analisis_form(request):
    anal = Analisis.objects.filter().values_list('NumAnali', flat=True).last()
    if anal == None:
        Numanal = 1
    else:
        Numanal = anal + 1
    context = {
        "NumAnal": Numanal,
    }
    if request.method == 'POST':
        anali = Analisis()
        new_name = request.POST.get('name',False)
        anali.NumAnali = Numanal
        anali.NomAnali = new_name
        anali.save()
        return HttpResponseRedirect(reverse('analisis_list'))
    return render(request, 'GBAPP/New/new_analisis_form.html', context)

@login_required()
def analisisestado_detail(request, analisise_id):
    analesta = get_object_or_404(AnalisisE, pk=analisise_id)
    context = {
        "analestado": analesta,
    }
    return render(request, 'GBAPP/Details/analisisestado_detail.html', context)

@login_required()
def analisisestado_detail(request, analisise_id):
    analesta = get_object_or_404(AnalisisE, pk=analisise_id)
    context = {
        "analestado": analesta,
    }
    return render(request, 'GBAPP/Details/analisisestado_detail.html', context)

@login_required()
def analisisestado_update(request, analisis_id):
    anal = get_object_or_404(AnalisisE, pk=analisis_id)
    new_aci = request.POST.get('aci',False)
    new_ph = request.POST.get('ph',False)
    new_grad = request.POST.get('grad',False)
    new_vin = request.POST.get('vin', False)
    new_cuar = request.POST.get('cuar', False)
    anal.PH = new_ph
    anal.AcidezTotal = new_aci
    anal.GradBaume = new_grad
    anal.NumVin = vinedo(id=new_vin)
    anal.NumCar = Cuartel(id=new_cuar)
    anal.save()
    return HttpResponseRedirect(reverse('analisisestado_list'))


@login_required()
def cuarteles_list(request,NumerVin):
    cuart = Cuartel.objects.filter(NumVin__NumeroVin=NumerVin)
    NumVin = get_object_or_404(vinedo, NumeroVin=NumerVin)
    estvin = Estadovinedo.objects.all()
    context = {
        "numvin": NumVin,
        "cuart": cuart,
        "estvine": estvin
    }
    return render(request, 'GBAPP/Lists/cuarteles_list.html', context)

@login_required()
def cuartel_detail(request, NumeroVin, NumCuar):
    cuart = get_object_or_404(Cuartel, NumVin__NumeroVin=NumeroVin, NumCuartel=NumCuar)
    estvin = Estadovinedo.objects.all()
    context = {
        "cuart": cuart,
        "estvine": estvin
    }
    return render(request, 'GBAPP/Details/cuartel_detail.html', context)

@login_required()
def cuartel_update(request, NumeroVin, NumCuar):
    cuart = get_object_or_404(Cuartel, NumVin__NumeroVin=NumeroVin, NumCuartel=NumCuar)
    context = cuart.NumVin_id
    new_grad = request.POST.get('TelaAnti', False) == 'on'
    new_stat = request.POST.get('status', False)
    new_ano = request.POST.get('ano', False)
    cuart.TelaAntigranizo = new_grad
    cuart.Estado_id = int(new_stat)
    cuart.anoplant = new_ano
    cuart.save()
    url = reverse('cuarteles_list',args=[context])
    return redirect(url)

@login_required()
def new_cuartel_form(request, NumeroVin):
    cuarte = Cuartel.objects.filter(NumVin__NumeroVin=NumeroVin).values_list('NumCuartel', flat=True).last()
    var = Varietal.objects.all()
    if cuarte == None:
        new_cuarte = 1
    else:
        new_cuarte = cuarte + 1
    estvin = Estadovinedo.objects.all()
    context = {
        "var": var,
        "estvine": estvin,
        "new_cuart": new_cuarte,
        "numvin": NumeroVin,
    }
    if request.method == 'POST':
        cuart = Cuartel()
        cuart.NumCuartel = new_cuarte
        cuart.NumVin_id = NumeroVin
        new_grad = request.POST.get('TelaAnti', False) == 'on'
        new_stat = request.POST.get('status', False)
        new_var = request.POST.get('var', False)
        new_fec = request.POST.get('fec_crea')
        new_ano = request.POST.get('ano_plan')
        cuart.TelaAntigranizo = new_grad
        cuart.Estado_id = int(new_stat)
        cuart.variedad_id = int(new_var)
        cuart.anoplant = new_ano
        cuart.created_date = new_fec
        cuart.TipoRiego = "Goteo"
        cuart.save()
        url = reverse('cuarteles_list', args=[NumeroVin])
        return redirect(url)
    return render(request, 'GBAPP/New/new_cuartel_form.html', context)

@login_required()
def new_contmad_form(request):
    vin = vinedo.objects.filter(Estado=1)
    lastcont = ControlMadurez.objects.filter().values_list('NumContMad', flat=True).last()
    cuar_id = Cuartel.objects.filter()
    if lastcont == None:
        numcont = 1
    else:
        numcont = lastcont + 1
    context = {
        "vinedo": vin,
        "numcontmad": numcont,
    }
    if request.method == 'POST':
        conte = ControlMadurez()
        new_vinedo = request.POST.get('vinedo', False)
        new_cuartel = request.POST.get('cuartel', False)
        new_ph = request.POST.get('ph', False)
        new_aci = request.POST.get('aci', False)
        new_Gradbau = request.POST.get('Gradbau', False)
        new_var = request.POST.get('var', False)
        cuar_id = get_object_or_404(Cuartel, NumCuartel=new_cuartel, NumVin__NumeroVin=new_vinedo)
        conte.NumVin_id = int(new_vinedo)
        conte.NumCuar_id = int(cuar_id.pk)
        conte.Varietal_id = int(new_var)
        if int(new_ph) >= 7 and int(new_ph) <=9 and  int(new_aci) >= 7 and int(new_aci) <= 9 and int(new_Gradbau) >= 2 and int(new_Gradbau) <= 5:
                conte.Estado = 1
        conte.NumContMad = numcont
        conte.save()
        return HttpResponseRedirect(reverse('login_success'))
    return render(request, 'GBAPP/New/new_contmad_form.html', context)

@login_required()
def get_filtered_options_view(request):
    selecte = request.GET.get('selected_value')
    filtered_options = Cuartel.objects.filter(NumVin__NumeroVin=selecte, Estado=1)
    options = []
    for option in filtered_options:
        options.append({'id': option.NumCuartel, 'var_id': option.variedad.Nombre})
    return JsonResponse(options, safe=False)

@login_required
def get_tamano_tanq_view(request):
    selected = request.GET.get('selected_value')
    tanque = get_object_or_404(TanqueM, NumTanque=selected)
    response = {'LitrosTan': tanque.LitrosAct}
    return JsonResponse(response)

@login_required()
def calendario(request):
    form = Calendar()
    return render(request, 'GBAPP/test.html', {'form': form})

@login_required()
def cronograma_list(request):
    control = ControlMadurez.objects.filter(Estado=1)
    context = {
        "control_list": control,
    }
    return render(request, 'GBAPP/Lists/cronograma_list.html', context)

@login_required()
def cronograma_fecha(request, NumContMad):
    control = get_object_or_404(ControlMadurez, pk=NumContMad)
    cuart = get_object_or_404(Cuartel, NumVin_id=control.NumVin.NumeroVin, NumCuartel=control.NumCuar.NumCuartel)
    bod = Bodega.objects.all()
    camio = Camionero.objects.filter(Estado__Estado='Vigente')
    context = {
        "cronograma": control,
        "bode": bod,
        "cuart":cuart,
        "camion": camio,
    }
    return render(request, 'GBAPP/Details/cronograma_fecha.html', context)

@login_required()
def cronograma_fecha_update(request, NumContMad):
    control = get_object_or_404(ControlMadurez, pk=NumContMad)
    cuart = get_object_or_404(Cuartel, NumVin_id=control.NumVin.NumeroVin, NumCuartel=control.NumCuar.NumCuartel)
    numer = Cronograma.objects.filter().values_list('NumPrograma', flat=True).last()
    if numer == None:
        num = 1
    else:
        num = numer + 1
    bod = Bodega.objects.all()
    context = {
        "cronograma": control,
        "bode": bod,
        "cuart": cuart,
    }
    if request.method == 'POST':
        crono = Cronograma()
        new_capa = request.POST.get('capacidad', False)
        new_kg = request.POST.get('kg', False)
        new_bode = request.POST.get('bodega', False)
        new_date = request.POST.get('new_date')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        new_camion = request.POST.get('camion', False)
        bode = get_object_or_404(Bodega, pk=int(new_bode))
        bode.CantidadActual -= int(new_kg)
        bode.save()
        crono.NumPrograma = num
        crono.Camionero_id = int(new_camion)
        crono.InicioPrograma = start_date
        crono.FechaIngreso = new_date
        crono.FinPrograma = end_date
        crono.NumVin_id = int(control.NumVin.NumeroVin)
        crono.NumCuar_id = int(control.NumCuar.id)
        crono.Capacidad = new_capa
        crono.Cantidad = new_kg
        crono.NumBod_id = int(new_bode)
        crono.ControlMaduOk_id = int(control.NumContMad)
        crono.save()
        control.Estado = 0
        control.save()
        return HttpResponseRedirect(reverse('login_success  '))
    return render(request, 'GBAPP/Details/cronograma_fecha.html', context)

@login_required()
def new_camionero(request):
    estado = Estadovinedo.objects.all()
    context = {
        "est": estado,
    }
    if request.method == 'POST':
        cam = Camionero()
        new_name = request.POST.get('name', False)
        new_ape = request.POST.get('ape', False)
        new_pat = request.POST.get('pat', False)
        new_mod = request.POST.get('mod', False)
        new_stat = request.POST.get('status', False)
        cam.Nombre = new_name
        cam.Apellido = new_ape
        cam.ModeloCamion = new_mod
        cam.Patente = new_pat
        cam.Estado_id = int(new_stat)
        cam.save()
        return HttpResponseRedirect(reverse('login_success'))
    return render(request, 'GBAPP/New/new_camionero.html', context)

@login_required()
def new_tanque_tipo(request):
    if request.method == 'POST':
        tan = TipoTanq()
        new_name = request.POST.get('name', False)
        tan.TipoTanque = new_name
        tan.save()
        return HttpResponseRedirect(reverse('tanqueABM'))
    return render(request, 'GBAPP/New/new_tanque_tipo.html')

@login_required()
def new_tanque(request):
    tantipo = TipoTanq.objects.all()
    tanq = TanqueM.objects.filter().values_list('NumTanque', flat=True).last()
    if tanq == None:
        numtanq = 1
    else:
        numtanq = tanq + 1
    context = {
        "tantipo": tantipo,
        "numerotanque": str(numtanq)
    }
    if request.method == 'POST':
        tan = TanqueM()
        new_stat = request.POST.get('status', False)
        new_lts = request.POST.get('lit', False)
        tan.TipoTanque_id = int(new_stat)
        tan.LitrosTan = new_lts
        tan.NumTanque = numtanq
        tan.save()
        return HttpResponseRedirect(reverse('tanqueABM'))
    return render(request, 'GBAPP/New/new_tanque.html', context)

@login_required()
def bodega_pesada_list(request):
    pesada = Pesada.objects.filter(Eliminado="0").filter(Bascula="1")
    context = {
        "pesada_list": pesada,
    }
    return render(request, 'GBAPP/Lists/bodega_pesada_list.html', context)


@login_required()
def bodega_pesada_detail(request, pesada_id):
    pesada = get_object_or_404(Pesada, pk=pesada_id)
    cuart = get_object_or_404(Cuartel, NumVin_id=pesada.Vinedo.NumeroVin, NumCuartel=pesada.Cuartel.NumCuartel)
    prensada = TanqueM.objects.filter(TipoTanque_id="1")
    lts = int(pesada.PesoNeto) * 0.6
    context = {
        "lts": lts,
        "pesada": pesada,
        "cuart_list": cuart,
        "prensada": prensada,
    }
    return render(request, 'GBAPP/Details/bodega_pesada_detail.html', context)

@login_required()
def bodega_pesada_update(request, pesada_id):
    #/// ERA SOLO POR LA BARRA EN URL.PY /// FALTAN AGREGA DATOS Y HACER CUADROS TILDE PARA OPCIONES DE ESTADOS
    pesada = get_object_or_404(Pesada, pk=pesada_id)
    mov = TanqueE.objects.filter().values_list('NumeroMov', flat=True).last() or 0
    ord = TanqueE.objects.filter().values_list('NumeroOrden', flat=True).last() or 0
    new_mov = mov + 1
    new_ord = ord + 1
    tanqe = TanqueE()
    if request.method == 'POST':
        lts = int(pesada.PesoNeto) * 0.65
        new_prensa = request.POST.get('prensa', False)
        tanqm = get_object_or_404(TanqueM, NumTanque=new_prensa)
        tanqm.LitrosAct = int(tanqm.LitrosTan) - lts
        tanqm.save()
        tanqe.LitrosOcupados = lts
        tanqe.NumeroMov = new_mov
        tanqe.PesaInicial_id = int(pesada.NumeroPesada)
        tanqe.EstadoAnalisis = 0
        tanqe.EstadoCorte = 0
        tanqe.EstadoPrensada = 1
        tanqe.EstadoFermentacion = 0
        tanqe.EstadoRemontaje = 0
        tanqe.NumeroOrden = new_ord
        tanqe.TanqueMa_id = int(new_prensa)
        pesada.Eliminado = 1
        pesada.save()
        tanqe.save()
        return HttpResponseRedirect(reverse('bodegaABM'))
    return render(request, 'GBAPP/Details/bodega_pesada_detail.html')

@login_required()
def bodega_movimientos_list(request):
    movi = TanqueE.objects.exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1).exclude(TanqueMa__TipoTanque_id="5")
    context = {
        "mov_list": movi,
    }
    return render(request, 'GBAPP/Lists/bodega_movimientos_list.html', context)

@login_required()
def bodega_movimientos_detail(request, orden_id, num_tanq):
    # MOVIMIENTOS ENTRE TANQUES (CORTES)
    mov = get_object_or_404(TanqueE, NumeroOrden=orden_id, TanqueMa=num_tanq, Eliminado=0)
    tanqm = TanqueM.objects.exclude(TipoTanque_id="1").exclude(NumTanque=mov.TanqueMa.NumTanque).exclude(TipoTanque_id__exact=5)
    context = {
        "datamov": mov,
        "tanqm": tanqm,
    }
    return render(request, 'GBAPP/Details/bodega_movimientos_detail.html', context)

@login_required()
def bodega_movimientos_update(request, orden_id, num_tanq):
    #ACTUALIZACION DE MOVIMIENTOS ENTRE TANQUES, DEBE GUARADR EN TANQUEE LA LINEA DE MOVIMIENTO DEJANDO ACENTADO HISTORIAL EN TANQACT
    mov = get_object_or_404(TanqueE, NumeroOrden=orden_id, TanqueMa=num_tanq, Eliminado=0)

    tanq = TanqueE.objects.filter().values_list('NumeroMov', flat=True).last() or 0
    ord = TanqueE.objects.filter().values_list('NumeroOrden', flat=True).last() or 0
    new_tanq = tanq + 1

    if request.method == 'POST':

        new_tanqu = request.POST.get('tanq', False)
        new_lts = request.POST.get('lts', False)

        nm = get_object_or_404(TanqueM, NumTanque=num_tanq)
        nta = get_object_or_404(TanqueM, NumTanque=new_tanqu)

        tanqe = TanqueE()
        tanqe.NumeroMov = new_tanq
        tanqe.PesaInicial_id = mov.PesaInicial_id
        tanqe.LitrosOcupados = int(new_lts) + (int(nta.LitrosTan) - int(nta.LitrosAct))
        tanqe.EstadoAnalisis = 0
        tanqe.EstadoPrensada = 1
        tanqe.EstadoFermentacion = 0
        tanqe.EstadoRemontaje = 0
        tanqe.TanqueMa_id = int(nta.NumTanque)

        tanact = TanqAct()
        tanact.LitrosMov = new_lts
        tanact.MovPrevTanque_id = int(mov.TanqueMa.NumTanque)
        tanact.MovPosTanque_id = int(nta.NumTanque)
        tanact.save()

        nm.LitrosAct += int(new_lts)
        nm.save()
        mov.LitrosOcupados -= int(new_lts)
        mov.save()

        if nta.LitrosTan == nta.LitrosAct:
            tanqe.EstadoCorte = 0
            tanqe.NumeroOrden = mov.NumeroOrden
            nta.LitrosAct = int(nta.LitrosTan) - int(new_lts)
            tanqe.save()
            tanact.NumeroOrd.add(tanqe)
        else:
            tanqe.EstadoCorte = 1
            lasttan = TanqueE.objects.filter(TanqueMa=new_tanqu).aggregate(Max('NumeroOrden'))['NumeroOrden__max']
            tanque_e_object = TanqueE.objects.get(TanqueMa=new_tanqu, NumeroOrden=lasttan)
            tanqe.NumeroOrden = ord + 1
            nta.LitrosAct -= int(new_lts)
            tanque_e_object.Eliminado = 1
            tanque_e_object.save()
            tanqe.save()
            new_numeroo = TanqueE.objects.filter().values_list('NumeroOrden', flat=True).last() or 0
            tanact.NumeroOrd.add(new_numeroo + 1)
        tanact.save()
        nta.save()
        return HttpResponseRedirect(reverse('bodega_movimientos_list'))
    return render(request, 'GBAPP/Details/bodega_movimientos_detail.html')

@login_required()
def aditamentos_list(request):

    adit = TanqueE.objects.exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1)
    anali = Analisis.objects.all()
    context = {
        "adit": adit,
        "prensada": anali,
    }
    return render(request, 'GBAPP/Lists/aditamentos_list.html', context)


@login_required()
def aditamentos_detail(request, orden_id):
    #DETALLE DE TANQUE PARA AGREGAR ANALISIS
    adit = get_object_or_404(TanqueE, pk=orden_id)
    tanqm = TanqueM.objects.exclude(TipoTanque_id="1").exclude(NumTanque=adit.TanqueMa.NumTanque)
    anal = Analisis.objects.all()
    context = {
        "adit": adit,
        "tanqm": tanqm,
        "anali":anal,
    }
    return render(request, 'GBAPP/Details/aditamentos_detail.html', context)

@login_required()
def aditamentos_update(request, orden_id):
    # REVISAR FALTA AGREGAR DATOS PARA GUARDAR EN TANQUEE
    adit = get_object_or_404(TanqueE, pk=orden_id)
    tanqm = TanqueM.objects.exclude(TipoTanque_id="1").exclude(NumTanque=adit.TanqueMa.NumTanque)
    anal = Analisis.objects.all()
    context = {
        "adit": adit,
        "tanqm": tanqm,
        "anali": anal,
    }
    if request.method == 'POST':

        new_statremon = request.POST.get('statremon', False)
        new_statpren = request.POST.get('statpren', False)
        new_statcor = request.POST.get('statcor', False)
        new_estaana = request.POST.get('estaana', False)
        new_anali = request.POST.get('anali', False)


        new_tanqu = request.POST.get('tanq', False)
        new_lts = request.POST.get('lts', False)

        nm = get_object_or_404(TanqueM, NumTanque=num_tanq)
        nta = get_object_or_404(TanqueM, NumTanque=new_tanqu)

        tanqe = TanqueE()
        tanqe.NumeroMov = new_tanq
        tanqe.PesaInicial_id = mov.PesaInicial_id
        tanqe.LitrosOcupados = int(new_lts) + (int(nta.LitrosTan) - int(nta.LitrosAct))
        tanqe.EstadoAnalisis = 0
        tanqe.EstadoPrensada = 1
        tanqe.EstadoFermentacion = 0
        tanqe.EstadoRemontaje = 0
        tanqe.TanqueMa_id = int(nta.NumTanque)

        tanact = TanqAct()
        tanact.LitrosMov = new_lts
        tanact.MovPrevTanque_id = int(mov.TanqueMa.NumTanque)
        tanact.MovPosTanque_id = int(nta.NumTanque)
        tanact.save()

        nm.LitrosAct += int(new_lts)
        nm.save()
        mov.LitrosOcupados -= int(new_lts)
        mov.save()

        if nta.LitrosTan == nta.LitrosAct:
            tanqe.EstadoCorte = 0
            tanqe.NumeroOrden = mov.NumeroOrden
            nta.LitrosAct = int(nta.LitrosTan) - int(new_lts)
            tanqe.save()
            tanact.NumeroOrd.add(tanqe)
        else:
            tanqe.EstadoCorte = 1
            lasttan = TanqueE.objects.filter(TanqueMa=new_tanqu).aggregate(Max('NumeroOrden'))['NumeroOrden__max']
            tanque_e_object = TanqueE.objects.get(TanqueMa=new_tanqu, NumeroOrden=lasttan)
            tanqe.NumeroOrden = ord + 1
            nta.LitrosAct -= int(new_lts)
            tanque_e_object.Eliminado = 1
            tanque_e_object.save()
            tanqe.save()
            new_numeroo = TanqueE.objects.filter().values_list('NumeroOrden', flat=True).last() or 0
            tanact.NumeroOrd.add(new_numeroo + 1)
        tanact.save()
        nta.save()

        return HttpResponseRedirect(reverse('aditamentos_list'))
    return render(request, 'GBAPP/Details/aditamentos_detail.html', context)


@login_required()
def stock(request):
    stock = get_object_or_404(Stock, pk=1)
    context = {
        "sto": stock,
    }
    if request.method == 'POST':
        new_bot = request.POST.get('CantBot', False)
        new_sep = request.POST.get('CantSepa', False)
        new_cor = request.POST.get('CantCorchos', False)
        new_eti = request.POST.get('CantEtiquetas', False)
        stock.CantSepara = int(new_sep) + int(stock.CantSepara)
        stock.CantCorcho = int(new_cor) + int(stock.CantCorcho)
        stock.CantEtiqueta = int(new_eti) + int(stock.CantEtiqueta)
        stock.CantBot = int(new_bot) + int(stock.CantBot)
        stock.save()
    return render(request, 'GBAPP/New/new_stock.html', context)


@login_required()
def stockfraccionado(request):
    emb = Franccionado.objects.filter().values_list("NumEmbo", flat=True).last()
    frac = get_object_or_404(Franccionado, pk=2)
    context = {
        "frac": frac,
    }
    if emb == None:
        new_emb = 1
    else:
        new_emb = emb + 1
    frac = Franccionado()
    if request.method == 'POST':
        new_bot = request.POST.get('CantBot', False)
        new_sep = request.POST.get('CantSepa', False)
        new_cor = request.POST.get('CantCorchos', False)
        new_eti = request.POST.get('CantEtiquetas', False)
        frac.NumEmbo = new_emb
        frac.CantSepara = new_sep
        frac.CantCorcho = new_cor
        frac.CantEtiqueta = new_eti
        frac.TipoBot = "Verde"
        frac.TipoCaj = "Carton"
        frac.TipoSepara = "Telgopor"
        frac.Articulo = "Vino"
        frac.CantBot = new_bot
        frac.save()
    return render(request, 'GBAPP/New/new_stock.html', context)

@login_required()
def fraccionado_list(request):
    # adit = TanqueE.objects.exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1)
    tanq = TanqueE.objects.filter(TanqueMa__TipoTanque_id="5")
    context = {
        "tanq_list": tanq,
    }
    return render(request, 'GBAPP/Lists/fraccionado_list.html', context)

@login_required()
def tanquefraccionado_list(request):
    adit = TanqueE.objects.exclude(TanqueMa__TipoTanque_id="5").exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1)
    context = {
        "tanq_list": adit,
    }
    return render(request, 'GBAPP/Lists/tanquefraccionado_list.html', context)

@login_required()
def tanquefraccionado_detail(request, orden_id):
    adit = get_object_or_404(TanqueE, pk=orden_id)
    adit = TanqueE.objects.exclude(TanqueMa__TipoTanque_id="5").exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1)
    anal = Analisis.objects.all()
    context = {
        "adit": adit,
        "tanqm": tanqm,
        "anali":anal,
    }
    return render(request, 'GBAPP/Details/aditamentos_detail.html', context)


@login_required()
def trazabilidad_list(request):
    adit = TanqueE.objects.exclude(TanqueMa__TipoTanque_id="5").exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1)
    context = {
        "tanq_list": adit,
    }
    return render(request, 'GBAPP/Lists/tanquefraccionado_list.html', context)

@login_required()
def trazabilidad_detail(request, orden_id):
    adit = get_object_or_404(TanqueE, pk=orden_id)
    adit = TanqueE.objects.exclude(TanqueMa__TipoTanque_id="5").exclude(TanqueMa__LitrosTan__exact=F('TanqueMa__LitrosAct')).exclude(Eliminado=1)
    anal = Analisis.objects.all()
    context = {
        "adit": adit,
        "tanqm": tanqm,
        "anali":anal,
    }
    return render(request, 'GBAPP/Details/aditamentos_detail.html', context)