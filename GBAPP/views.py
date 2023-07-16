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
    prod = get_object_or_404(Cuartel, pk=1)
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
    vin.delete()
    return HttpResponseRedirect(reverse('vinedo_list'))

@login_required()
def pesada_detail(request, pesada_id):
    pesada = get_object_or_404(Pesada, pk=pesada_id)
    camionero = Camionero.objects.filter(Estado__Estado='Vigente')
    variet = Varietal.objects.all()
    vin = vinedo.objects.filter(Estado__Estado='Vigente')
    context = {
        "pesada_list": pesada,
        "camionero_list": camionero,
        "varietal": variet,
        "vinedo": vin,
    }
    return render(request, 'GBAPP/Details/pesada_detail.html', context)

@login_required()
def pesada_update(request, pesada_id):
    pes = get_object_or_404(Pesada, pk=pesada_id)
    new_tara = request.POST.get('Tara', False)
    new_bruto = request.POST.get('PesoBruto', False)
    new_pesnet = int(new_bruto) - int(new_tara)
    pes.Tara = new_tara
    pes.PesoNeto = new_pesnet
    pes.PesoBruto = new_bruto
    if new_pesnet > 0:
        pes.Bascula = 1
    pes.save()
    return HttpResponseRedirect(reverse('pesada_list'))

@login_required()
def pesada_list(request):
    pesada = Pesada.objects.filter(Eliminado="0").filter(Bascula="0")
    context = {
        "pesada_list": pesada,
    }
    return render(request, 'GBAPP/Lists/pesada_list.html', context)

def buscarpesada_view(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Pesada.objects.filter(Vinedo__Nombre__icontains=query)

    return render(request, 'GBAPP/Busqueda/buscar_pesada.html', {'form': form, 'results': results})

@login_required()
def new_pesada_form(request):
    lastnumpes = Pesada.objects.filter().values_list('NumeroPesada', flat=True).last()
    NumPes = lastnumpes + 1
    cre_date = datetime.today()
    camio = Camionero.objects.filter(Estado__Estado='Vigente')
    variet = Varietal.objects.all()
    vin = vinedo.objects.filter(Estado__Estado='Vigente')
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
    return render(request, 'GBAPP/New/new_pesada_form.html', context)

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
    NumVin = vinedo.objects.filter(NumeroVin=NumerVin)
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
def new_cuartel_form(request):
    lastnumvin = Cuartel.objects.filter().values_list('NumCuartel', flat=True).last()
    Numvin = lastnumvin + 1
    cre_date = datetime.today()
    estvin = Estadovinedo.objects.all()
    context = {
        "numvin": Numvin,
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
def new_contmad_form(request):
    vin = vinedo.objects.filter(Estado=1)
    var = Varietal.objects.all()
    lastcont = ControlMadurez.objects.filter().values_list('NumContMad', flat=True).last()
    numcont = int(lastcont) + 1
    initial_datetime = datetime.now()
    form = Calendar(initial={'my_datetime': initial_datetime})
    context = {
        "vinedo": vin,
        "numcontmad": numcont,
        "variedad": var,
        "form": form,
    }
    if request.method == 'POST':
        conte = ControlMadurez()
        new_vinedo = request.POST.get('vinedo', False)
        new_cuartel = request.POST.get('cuartel', False)
        new_ph = request.POST.get('ph', False)
        new_aci = request.POST.get('aci', False)
        new_Gradbau = request.POST.get('Gradbau', False)
        new_var = request.POST.get('var', False)
        conte.NumVin_id = int(new_vinedo)
        conte.NumCuar_id = int(new_cuartel)
        conte.Varietal_id = int(new_var)
        if int(new_ph) >= 8 and int(new_ph) <=9:
            if int(new_aci) >= 7 and int(new_aci) <= 9:
                if int(new_Gradbau) >= 2 and int(new_Gradbau) <= 5:
                        conte.Estado = 1
        conte.NumContMad = numcont
        conte.save()
        return HttpResponseRedirect(reverse('new_contmad'))
    return render(request, 'GBAPP/New/new_contmad_form.html', context)

@login_required()
def get_filtered_options_view(request):
    selecte = request.GET.get('selected_value')
    filtered_options = Cuartel.objects.filter(NumVin__NumeroVin=selecte, Estado__cuartel=1)
    options = []
    for option in filtered_options:
        options.append({'id': option.NumCuartel})
    return JsonResponse(options, safe=False)

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
    bod = Bodega.objects.all()
    context = {
        "cronograma": control,
        "bode": bod,
    }
    return render(request, 'GBAPP/Details/cronograma_fecha.html', context)

@login_required()
def cronograma_fecha_update(request, NumContMad):
    control = get_object_or_404(ControlMadurez, pk=NumContMad)
    numer = Cronograma.objects.filter().values_list('NumPrograma', flat=True).last()
    num = numer + 1
    bod = Bodega.objects.all()
    context = {
        "cronograma": control,
        "bode": bod,
    }
    if request.method == 'POST':
        crono = Cronograma()
        new_capa = request.POST.get('capacidad', False)
        new_kg = request.POST.get('kg', False)
        new_bode = request.POST.get('bodega', False)
        new_date = request.POST.get('new_date')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        crono.NumPrograma = num
        crono.InicioPrograma = start_date
        crono.FechaIngreso = new_date
        crono.FinPrograma = end_date
        crono.NumVin_id = int(control.NumVin.NumeroVin)
        crono.NumCuar_id = int(control.NumCuar.NumCuartel)
        crono.Capacidad = new_capa
        crono.Cantidad = new_kg
        crono.NumBod_id = int(new_bode)
        crono.ControlMaduOk_id = int(control.NumContMad)
        crono.save()
        control.Estado = 0
        control.save()
        return HttpResponseRedirect(reverse('cronograma_list'))
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
    tanque = TanqueM.objects.filter().values_list('NumTanque', flat=True).last()
    numtanq = int(tanque) + 1
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
    prensada = TanqueM.objects.filter(TipoTanque_id="1")
    context = {
        "pesada_list": pesada,
        "prensada": prensada,
    }
    return render(request, 'GBAPP/Details/bodega_pesada_detail.html', context)

@login_required()
def bodega_pesada_update(request, pesada_id):
    #/// ERA SOLO POR LA BARRA EN URL.PY /// NO FUNCIONABA
    pesada = get_object_or_404(Pesada, pk=pesada_id)
    tanq = TanqueE.objects.filter().values_list('NumeroMov', flat=True).last()
    new_tanq = tanq + 1
    tanqe = TanqueE()
    if request.method == 'POST':
        new_prensa = request.POST.get('prensa', False)
        tanqe.LitrosOcupados = int(pesada.PesoNeto) * 0.6
        tanqe.NumeroMov = new_tanq
        tanqe.PesaInicial_id = int(pesada.NumeroPesada)
        tanqe.EstadoAnalisis = 0
        tanqe.EstadoCorte = 0
        tanqe.EstadoPrensada = 1
        tanqe.EstadoFermentacion = 0
        tanqe.EstadoRemontaje = 0
        tanqe.NumeroOrden = 2
        tanqe.TanqueMa_id = int(new_prensa)
        pesada.Eliminado = 1
        pesada.save()
        tanqe.save()
        return HttpResponseRedirect(reverse('bodega_pesada_list'))
    return render(request, 'GBAPP/Details/bodega_pesada_detail.html')

@login_required()
def bodega_movimientos_list(request):
    movi = TanqueE.objects.all()
    prensada = TanqueM.objects.exclude(TipoTanque_id="1")
    context = {
        "mov_list": movi,
        "prensada": prensada,
    }
    return render(request, 'GBAPP/Lists/bodega_movimientos_list.html', context)

@login_required()
def bodega_movimientos_detail(request, orden_id):
    # MOVIMIENTOS ENTRE TANQUES (CORTES)
    # TERMINAR DE AGREGAR DATOS MOVIMIENTOS
    mov = get_object_or_404(TanqueE, pk=orden_id)
    tanqm = TanqueM.objects.exclude(TipoTanque_id="1").exclude(NumTanque=mov.TanqueMa.NumTanque)
    context = {
        "datamov": mov,
        "tanqm": tanqm,
    }
    return render(request, 'GBAPP/Details/bodega_movimientos_detail.html', context)

@login_required()
def bodega_movimientos_update(request, pesada_id):
    #ACTUALIZACION DE MOVIMIENTOS ENTRE TANQUES, DEBE GUARADR EN TANQUEE LA LINEA DE MOVIMIENTO DEJANDO ACENTADO HISTORIAL EN TANQACT
    pesada = get_object_or_404(Pesada, pk=pesada_id)
    tanq = TanqueE.objects.filter().values_list('NumeroMov', flat=True).last()
    new_tanq = tanq + 1
    tanqe = TanqueE()
    if request.method == 'POST':
        new_prensa = request.POST.get('prensa', False)
        tanqe.LitrosOcupados = int(pesada.PesoNeto) * 0.6
        tanqe.NumeroMov = new_tanq
        tanqe.PesaInicial_id = int(pesada.NumeroPesada)
        tanqe.EstadoAnalisis = 0
        tanqe.EstadoCorte = 0
        tanqe.EstadoPrensada = 1
        tanqe.EstadoFermentacion = 0
        tanqe.EstadoRemontaje = 0
        tanqe.NumeroOrden = 2
        tanqe.TanqueMa_id = int(new_prensa)
        pesada.Eliminado = 1
        pesada.save()
        tanqe.save()
        return render(request, 'GBAPP/Details/vinedo_detail.html')
    return render(request, 'GBAPP/Details/vinedo_detail.html')

@login_required()
def aditamentos_list(request):
    adit = TanqueE.objects.all()
    prensada = TanqueM.objects.exclude(TipoTanque_id="1")
    anali = AnalisisE.objects.all()
    context = {
        "adit": adit,
        "prensada": prensada,
    }
    return render(request, 'GBAPP/Lists/aditamentos_list.html', context)


@login_required()
def aditamentos_detail(request, orden_id):
    #DETALLE DE TANQUE PARA AGREGAR ANALISIS
    # A ESTE COMO FINAL AGREGAR ADITAMENTOS
    adit = get_object_or_404(TanqueE, pk=orden_id)
    tanqm = TanqueM.objects.exclude(TipoTanque_id="1").exclude(NumTanque=adit.TanqueMa.NumTanque)
    context = {
        "adit": adit,
        "tanqm": tanqm,
    }
    return render(request, 'GBAPP/Details/aditamentos_detail.html', context)

@login_required()
def aditamentos_update(request, pesada_id):
    # AGREGAR ADITAMENTOS A TANQUES PARA MEJORAR VINO,
    # POST ANALISIS SE GENERA VENTANA PARA AGREGAR ADITAMENTOS
    # (SOLO FLAG PARA AVISAR DE ADITAMENTOS, PERO NO SE GUARDAN)
    # pesada = get_object_or_404(Pesada, pk=pesada_id)
    # tanq = TanqueE.objects.filter().values_list('NumeroMov', flat=True).last()
    # new_tanq = tanq + 1
    # tanqe = TanqueE()
    if request.method == 'POST':

        return render(request, 'GBAPP/Details/aditamentos_detail.html')
    return render(request, 'GBAPP/Details/aditamentos_detail.html')

@login_required()
def aditamentos_add(request):
    adit = TanqueE.objects.all()
    context = {
        "mov_list": adit,
    }
    return render(request, 'GBAPP/Lists/aditamentos_add.html', context)


@login_required()
def stockfraccionado(request):
    emb = Franccionado.objects.filter().values_list("NumEmbo", flat=True).last()
    frac = get_object_or_404(Franccionado, pk=2)
    cre_date = datetime.today()
    context = {
        "frac": frac,
    }
    if emb == None:
        emb = 1
        new_emb = emb + 1
    else:
        new_emb = emb + 1
    frac = Franccionado()
    if request.method == 'POST':
        new_bot = request.POST.get('CantBot', False)
        new_sep = request.POST.get('CantSepa', False)
        new_cor = request.POST.get('CantCorchos', False)
        new_eti = request.POST.get('CantEtiquetas', False)
        frac.NumEmbo = new_emb
        frac.FinProc = cre_date
        frac.IniProc = cre_date
        frac.CantSepara = new_sep
        frac.CantCorcho = new_cor
        frac.CantEtiqueta = new_eti
        frac.TipoBot = "Verde"
        frac.TipoCaj = "Carton"
        frac.TipoSepara = "Telgopor"
        frac.Articulo = "Vino"
        frac.CantBot = new_bot
        frac.save()
    return render(request, 'GBAPP/New/new_fraccionado.html', context)