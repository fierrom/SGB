# Generated by Django 4.2.1 on 2023-07-17 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0050_remove_controlmadurez_varietal'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanquem',
            name='LitrosAct',
            field=models.IntegerField(default=0),
        ),
    ]