# Generated by Django 4.2.1 on 2023-07-09 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0034_remove_tanqact_movitannum_tanqact_numeroord_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanqact',
            name='MoviTanNum',
        ),
        migrations.RemoveField(
            model_name='tanquee',
            name='EstadoFermentacion',
        ),
    ]