# Generated by Django 4.2.1 on 2023-07-01 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0002_analisise_gradbaume_analisise_numcuar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlmadurez',
            name='Estado',
            field=models.BooleanField(default=False),
        ),
    ]