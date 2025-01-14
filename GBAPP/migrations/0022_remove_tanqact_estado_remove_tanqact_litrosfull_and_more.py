# Generated by Django 4.2.1 on 2023-07-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0021_remove_tanqact_estado_remove_tanqact_litrosfull_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanqact',
            name='Estado',
        ),
        migrations.RemoveField(
            model_name='tanqact',
            name='LitrosFull',
        ),
        migrations.RemoveField(
            model_name='tanqact',
            name='LitrosPorcentaje',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstTanque',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoClari',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoCrianza',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoDespalillado',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoEstrujado',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoMacerado',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoTrasciego',
        ),
        migrations.AddField(
            model_name='tanqact',
            name='LitrosMov',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tanqact',
            name='MovPosTanque',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tanqact',
            name='MovPrevTanque',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tanqact',
            name='MoviTanNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tanquee',
            name='EstadoAnalisis',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tanquee',
            name='EstadoCorte',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tanquee',
            name='EstadoRemontaje',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tanquee',
            name='LitrosOcupados',
            field=models.IntegerField(default=0),
        ),
    ]
