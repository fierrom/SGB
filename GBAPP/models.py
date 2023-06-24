from django.db import models
from django.utils import timezone


class Estadovinedo(models.Model):
    Estado = models.CharField(max_length=50)

    def __str__(self):
        return self.Estado


class vinedo(models.Model):
    Dueno = models.TextField(max_length=50)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=50)
    NumeroVin = models.IntegerField(primary_key=True, unique=True)
    Ubicacion = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    """mod_date = models.DateTimeField(
            blank=True, null=True)"""

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumeroVin


class Cosecha(models.Model):
    Calidad = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    NumeroCosecha = models.IntegerField()
    Variedad = models.CharField(max_length=50)

    def __str__(self):
        return self.NumeroCosecha


class Cuartel(models.Model):
    NumVin = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    CantHileras = models.IntegerField()
    NumCuart = models.IntegerField()
    VarUva = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumCuart


class Hilera(models.Model):
    NumCuart = models.ForeignKey(Cuartel, on_delete=models.CASCADE)
    CantHileras = models.IntegerField()
    NumHil = models.IntegerField()

    def __int__(self):
        return self.NumHil


class Planta(models.Model):
    NumHil = models.ForeignKey(Hilera, on_delete=models.CASCADE)
    NumPlanta = models.IntegerField()
    CantPlantas = models.IntegerField()
    PorcEnvero = models.IntegerField()
    PorcFloracion = models.IntegerField()
    Enfermedades = models.CharField(max_length=50)
    HojaAmarilla = models.BooleanField()
    Obs = models.CharField(max_length=50)
    PesoMedBaya = models.IntegerField()
    Temperatura = models.IntegerField()

    def __int__(self):
        return self.NumPlanta


class Proceso(models.Model):
    NumCose = models.ForeignKey(Cosecha, on_delete=models.CASCADE)
    NumProc = models.IntegerField()
    VarUva = models.ForeignKey(Cuartel, on_delete=models.CASCADE)
    IniProc = models.DateTimeField(default=timezone.now)
    FinProc = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumProc


class Tanque(models.Model):
    Cosecha = models.ForeignKey(Cosecha, on_delete=models.CASCADE)
    NumTanque = models.IntegerField()
    LitrosTan = models.IntegerField()
    LitrosFill = models.IntegerField()
    LitrosPorcentaje = models.IntegerField()


    def __int__(self):
        return self.NumTanque

class Movimientos(models.Model):
    NumMov = models.IntegerField()
    TanqInicio = models.IntegerField()
    TanqFinal = models.IntegerField()

    def __int__(self):
        return self.NumMov


class TanqAct(models.Model):
    Estado = models.CharField(max_length=50)

    def __str__(self):
        return self.Estado


class TanqueEstado(models.Model):
    EstadoClari = models.BooleanField()
    NumTanque = models.ForeignKey(Tanque, on_delete=models.CASCADE)
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


class Trazabilidad(models.Model):
    NumTrazabilidad = models.IntegerField()
    NumTanque = models.ForeignKey(Tanque, on_delete=models.CASCADE)
    EstadoCrianza = models.BooleanField()
    EstadoDespalillado = models.BooleanField()
    EstadoEstrujado = models.BooleanField()
    EstadoFermentacion = models.BooleanField()
    EstadoMacerado = models.BooleanField()
    EstadoTrasciego = models.BooleanField()
    MovTanques = models.ForeignKey(Movimientos, on_delete=models.CASCADE)

    def __int__(self):
        return self.NumTrazabilidad


class Embotellado(models.Model):
    Articulo = models.CharField(max_length=50)
    CantBot = models.IntegerField()
    NumEmbo = models.CharField(max_length=50)
    IdProc = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    Tanque = models.ForeignKey(Tanque, on_delete=models.CASCADE)
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

class Varietal(models.Model):
    Nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre
class Pesada(models.Model):
    NumeroPesada = models.IntegerField()
    Camionero = models.ForeignKey(Camionero, on_delete=models.CASCADE)
    Tara = models.IntegerField()
    PesoNeto = models.IntegerField()
    PesoBruto = models.IntegerField()
    Vinedo = models.ForeignKey(vinedo, on_delete=models.CASCADE, to_field='NumeroVin')
    Varietal = models.ForeignKey(Varietal, on_delete=models.CASCADE)
    FechaCosecha = models.DateTimeField(default=timezone.now)

    def __int__(self):
        return self.NumeroPesada