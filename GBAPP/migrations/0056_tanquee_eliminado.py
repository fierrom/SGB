# Generated by Django 4.2.1 on 2023-07-19 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0055_remove_analisise_tanqe_remove_tanqact_numeroord_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanquee',
            name='Eliminado',
            field=models.IntegerField(default=0),
        ),
    ]