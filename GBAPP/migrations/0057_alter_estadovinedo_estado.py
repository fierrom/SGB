# Generated by Django 4.2.1 on 2023-07-21 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0056_tanquee_eliminado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadovinedo',
            name='Estado',
            field=models.BooleanField(max_length=50),
        ),
    ]