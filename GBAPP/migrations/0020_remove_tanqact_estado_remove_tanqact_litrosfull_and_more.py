# Generated by Django 4.2.1 on 2023-07-08 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0019_remove_tanqact_estado_remove_tanqact_litrosfull_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanquee',
            name='id',
        ),
        migrations.AddField(
            model_name='tanquee',
            name='NumeroMov',
            field=models.IntegerField(default=1, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='tanquee',
            name='NumeroOrden',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tanquee',
            name='PorcentFull',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tanquee',
            name='EstadoFermentacion',
            field=models.BooleanField(default=False),
        ),
    ]