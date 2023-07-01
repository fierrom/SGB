# Generated by Django 4.2.1 on 2023-06-24 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0006_alter_pesada_vinedo_alter_vinedo_numerovin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesada',
            name='vinedo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GBAPP.vinedo'),
        ),
        migrations.AlterField(
            model_name='vinedo',
            name='NumeroVin',
            field=models.IntegerField(unique=True),
        ),
    ]
