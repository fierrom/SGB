# Generated by Django 4.2.1 on 2023-07-21 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0061_alter_controlmadurez_numcuar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesada',
            name='NumeroPesada',
            field=models.IntegerField(default=1, primary_key=True, serialize=False, unique=True),
        ),
    ]
