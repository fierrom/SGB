# Generated by Django 4.2.1 on 2023-06-24 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0005_varietal_pesada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesada',
            name='Vinedo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GBAPP.vinedo', to_field='NumeroVin'),
        ),
        migrations.AlterField(
            model_name='vinedo',
            name='NumeroVin',
            field=models.IntegerField(unique=True),
        ),
    ]
