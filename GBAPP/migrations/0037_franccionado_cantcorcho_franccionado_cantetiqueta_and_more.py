# Generated by Django 4.2.1 on 2023-07-10 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0036_analisise_tanqe'),
    ]

    operations = [
        migrations.AddField(
            model_name='franccionado',
            name='CantCorcho',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='franccionado',
            name='CantEtiqueta',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='franccionado',
            name='CantSepara',
            field=models.IntegerField(default=0),
        ),
    ]
