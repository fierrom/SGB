# Generated by Django 4.2.1 on 2023-07-02 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0005_cronograma_variedad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cronograma',
            name='variedad',
        ),
    ]