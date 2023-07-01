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
    NomAnali = models.CharField(max_length=50,default=None)


class vinedo(models.Model):
    Dueno = models.TextField(max_length=50)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=50)
    NumeroVin = models.IntegerField(unique=True, primary_key=True)
    Ubicacion = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    Altura = models.IntegerField(default=0)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumeroVin

class Cuartel(models.Model):
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    anoplant = models.IntegerField(default=0)
    NumCuart = models.IntegerField(unique=True, primary_key=True)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE,default=2)
    TipoRiego = models.CharField(max_length=50,default=None)
    TelaAntigranizo = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumCuart


class ControlMadurez(models.Model):
    NumContMad = models.IntegerField(unique=True, primary_key=True)
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    NumCuar = models.ForeignKey(Cuartel, on_delete=models.CASCADE, to_field='NumCuart')
    IniProc = models.DateTimeField(default=timezone.now)
    FinProc = models.DateTimeField(default=timezone.now)
    Estado = models.BooleanField(default=False)

    def __int__(self):
        return self.NumContMad

class AnalisisE(models.Model):
    NumAnali = models.ForeignKey(Analisis, on_delete=models.CASCADE,to_field='NumAnali')
    PH = models.IntegerField(default=0)
    AcidezTotal = models.IntegerField(default=0)
    GradBaume = models.IntegerField(default=0)
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    NumCuar = models.ForeignKey(Cuartel, on_delete=models.CASCADE, to_field='NumCuart')

class TanqueM(models.Model):
    tan = models.IntegerField()
    NumTanque = models.IntegerField()
    LitrosTan = models.IntegerField()
    LitrosFill = models.IntegerField()
    LitrosPorcentaje = models.IntegerField()

    def __int__(self):
        return self.NumTanque


class TanqAct(models.Model):
    Estado = models.CharField(max_length=50)

    def __str__(self):
        return self.Estado


class TanqueE(models.Model):
    EstadoClari = models.BooleanField()
    NumTanque = models.ForeignKey(TanqueM, on_delete=models.CASCADE)
    EstTanque = models.ForeignKey(TanqAct, on_delete=models.CASCADE)
    EstadoCrianza = models.BooleanField()
    EstadoDespalillado = models.BooleanField()
    EstadoEstrujado = models.BooleanField()
    EstadoFermentacion = models.BooleanField()
    EstadoMacerado = models.BooleanField()
    EstadoTrasciego = models.BooleanField()
    FechaClari = models.DateTimeField(default=timezone.now)
    FechaCrianza = models.DateTimeField(default=timezone.now)
    FechaDespa = models.DateTimeField(default=timezone.now)
    FechaEstru = models.DateTimeField(default=timezone.now)
    FechaFermen = models.DateTimeField(default=timezone.now)
    FechaMace = models.DateTimeField(default=timezone.now)
    FechaTra = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.EstTanque



class Franccionado(models.Model):
    Articulo = models.CharField(max_length=50)
    CantBot = models.IntegerField()
    NumEmbo = models.CharField(max_length=50)
    IniProc = models.DateTimeField(default=timezone.now)
    FinProc = models.DateTimeField(default=timezone.now)
    TipoBot = models.CharField(max_length=50)
    TipoCaj = models.CharField(max_length=50)
    TipoSepara = models.CharField(max_length=50)

    def __int__(self):
        return self.NumEmbo


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
    Varietal = models.ForeignKey(Varietal, on_delete=models.CASCADE)
    FechaCosecha = models.DateTimeField(default=timezone.now)
    Eliminado = models.BooleanField()

    def __int__(self):
        return self.NumeroPesada