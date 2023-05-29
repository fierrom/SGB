from django.conf import settings
from django.db import models
from django.utils import timezone

class Estadovinedo(models.Model):
    Estado = models.TextField()
    def __str__(self):
        return self.Estado
class vinedo(models.Model):
    Dueno = models.TextField(max_length=50)
    Estado = models.ForeignKey(Estadovinedo, on_delete=models.CASCADE)
    Nombre = models.TextField()
    NumeroVin = models.IntegerField()
    Ubicacion = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    """mod_date = models.DateTimeField(
            blank=True, null=True)"""

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __int__(self):
        return self.NumeroVin

class Cosecha (models.Model):
    Calidad = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    NumeroCosecha = models.IntegerField()
    Variedad = models.CharField(max_length=50)

    def __str__(self):
        return self.NumeroCosecha