# Generated by Django 4.2.1 on 2023-07-17 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0049_remove_pesada_varietal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlmadurez',
            name='Varietal',
        ),
    ]
