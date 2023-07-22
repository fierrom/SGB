# Generated by Django 4.2.1 on 2023-07-18 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0051_tanquem_litrosact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pesada',
            name='Camionero',
        ),
        migrations.AddField(
            model_name='cronograma',
            name='Camionero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GBAPP.camionero'),
            preserve_default=False,
        ),
    ]