from django.db import models
from django.utils import timezone


class Estadovinedo(models.Model):
    Estado = models.CharField(max_length=50)

    def __str__(self):
        return self.Estado


class Varietal(models.Model):
    Nombre = models.CharField(max_length=50)


class Analisis(models.Model):
    NumAnali = models.IntegerField(unique=True, primary_key=True)
    NomAnali = models.CharField(max_length=50, default=None)


class vinedo(models.Model):
    Dueno = models.TextField(max_length=50)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=50)
    NumeroVin = models.IntegerField(unique=True, primary_key=True)
    Ubicacion = models.CharField(max_length=50)
    created_date = models.DateField(default=timezone.now)
    Altura = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumeroVin


class Cuartel(models.Model):
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    anoplant = models.IntegerField(default=0)
    id = models.AutoField(unique=True, primary_key=True,)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE, default=2)
    TipoRiego = models.CharField(max_length=50, default=None)
    TelaAntigranizo = models.BooleanField(default=False)
    created_date = models.DateField(default=timezone.now)
    variedad = models.ForeignKey(Varietal, on_delete=models.CASCADE)
    NumCuartel = models.IntegerField(default=0)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.id


class ControlMadurez(models.Model):
    NumContMad = models.IntegerField(default=0,unique=True, primary_key=True)
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    NumCuar = models.ForeignKey(Cuartel, on_delete=models.CASCADE, to_field='id')
    IniProc = models.DateField(default=timezone.now)
    Estado = models.BooleanField(default=False)

    def __int__(self):
        return self.NumContMad


class TipoTanq(models.Model):
    TipoTanque = models.CharField(max_length=50)

class TanqueM(models.Model):
    TipoTanque = models.ForeignKey(TipoTanq, on_delete=models.CASCADE)
    NumTanque = models.AutoField(default=500, unique=True, primary_key=True)
    LitrosTan = models.IntegerField(default=0)

class Bodega(models.Model):
    NumBodega = models.IntegerField(default=0, unique=True, primary_key=True)
    Cantidadmaxdia = models.IntegerField(default=80000)
    CantidadActual = models.IntegerField(default=0)
    NomBod = models.CharField(max_length=50)

class Cronograma(models.Model):
    FechaIngreso = models.DateField(default=timezone.now)
    ControlMaduOk = models.ForeignKey(ControlMadurez, on_delete=models.CASCADE)
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    NumCuar = models.ForeignKey(Cuartel, on_delete=models.CASCADE, to_field='id')
    Cantidad = models.IntegerField(default=0)
    Capacidad = models.IntegerField(default=0)
    NumPrograma = models.IntegerField(default=0, primary_key=True, unique=True)
    NumBod = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    InicioPrograma = models.DateField(default=timezone.now)
    FinPrograma = models.DateField(default=timezone.now)
    Eliminado = models.BooleanField(default=False)

class Camionero(models.Model):
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE)
    ModeloCamion = models.CharField(max_length=50)
    Patente = models.CharField(max_length=50)

    def __str__(self):
        return self.Patente
class Pesada(models.Model):
    NumeroPesada = models.IntegerField(unique=True, primary_key=True)
    Camionero = models.ForeignKey(Camionero, on_delete=models.CASCADE)
    Tara = models.IntegerField()
    PesoNeto = models.IntegerField()
    PesoBruto = models.IntegerField()
    Vinedo = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    Cuartel = models.ForeignKey(Cuartel, on_delete=models.CASCADE)
    FechaCosecha = models.DateField(default=timezone.now)
    Eliminado = models.BooleanField(default=False)
    Bascula = models.BooleanField(default=False)

    def __int__(self):
        return self.NumeroPesada

class TanqueE(models.Model):
    LitrosOcupados = models.IntegerField(default=0)
    NumeroOrden = models.IntegerField(default=0, unique=True)
    NumeroMov = models.AutoField(default=5001, primary_key=True, unique=True)
    PorcentFull = models.IntegerField(default=0)
    EstadoRemontaje = models.BooleanField(default=False)
    EstadoAnalisis = models.BooleanField(default=False)
    EstadoCorte = models.BooleanField(default=False)
    EstadoPrensada = models.BooleanField(default=False)
    PesaInicial = models.ForeignKey(Pesada, on_delete=models.CASCADE,default=1)
    TanqueMa = models.ForeignKey(TanqueM, on_delete=models.CASCADE, default=500)

class AnalisisE(models.Model):
    NumAnali = models.ForeignKey(Analisis, on_delete=models.CASCADE, to_field='NumAnali')
    PH = models.IntegerField(default=0)
    AcidezTotal = models.IntegerField(default=0)
    GradBaume = models.IntegerField(default=0)
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    NumCuar = models.ForeignKey(Cuartel, on_delete=models.CASCADE, to_field='id')
    TanqE = models.ForeignKey(TanqueE, on_delete=models.CASCADE, to_field='NumeroOrden')


class TanqAct(models.Model):
    LitrosMov = models.IntegerField(default=0)
    MovPrevTanque = models.ForeignKey(TanqueE, on_delete=models.CASCADE, related_name='movimientoprevio')
    MovPosTanque = models.ForeignKey(TanqueE,  on_delete=models.CASCADE, related_name='movimientoposterior')
    NumeroOrd = models.ForeignKey(TanqueE, on_delete=models.CASCADE, to_field='NumeroOrden' , related_name='NumeroO')

class Franccionado(models.Model):
    Articulo = models.CharField(max_length=50)
    CantBot = models.IntegerField(default=0)
    NumEmbo = models.IntegerField(default=0)
    IniProc = models.DateField(default=timezone.now)
    FinProc = models.DateField(default=timezone.now)
    TipoBot = models.CharField(max_length=50)
    TipoCaj = models.CharField(max_length=50)
    TipoSepara = models.CharField(max_length=50)
    CantSepara = models.IntegerField(default=0)
    CantCorcho = models.IntegerField(default=0)
    CantEtiqueta = models.IntegerField(default=0)

    def __int__(self):
        return self.NumEmbo

class Stock(models.Model):
    CantBot = models.IntegerField(default=0)
    CantSepara = models.IntegerField(default=0)
    CantCorcho = models.IntegerField(default=0)
    CantEtiqueta = models.IntegerField(default=0)
