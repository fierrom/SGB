# Generated by Django 4.2.1 on 2023-07-16 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0039_cuartel_numcuartel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlmadurez',
            name='FinProc',
        ),
    ]
