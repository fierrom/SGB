# Generated by Django 4.2.1 on 2023-07-08 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0024_tanqact'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesada',
            name='Bascula',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pesada',
            name='Eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
