# Generated by Django 4.2.1 on 2023-07-02 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0006_remove_cronograma_variedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuartel',
            name='variedad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GBAPP.varietal'),
            preserve_default=False,
        ),
    ]