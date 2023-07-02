# Generated by Django 4.2.1 on 2023-07-02 03:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0003_controlmadurez_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('NumBodega', models.IntegerField(default=0, primary_key=True, serialize=False, unique=True)),
                ('Cantidadmax', models.IntegerField(default=80000)),
                ('CantidadActual', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cronograma',
            fields=[
                ('FechaIngreso', models.DateTimeField(default=django.utils.timezone.now)),
                ('Cantidad', models.IntegerField(default=0)),
                ('Capacidad', models.IntegerField(default=0)),
                ('NumPrograma', models.IntegerField(default=0, primary_key=True, serialize=False, unique=True)),
                ('ControlMaduOk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GBAPP.controlmadurez')),
                ('NumCuar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GBAPP.cuartel')),
                ('NumVin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GBAPP.vinedo')),
            ],
        ),
    ]
