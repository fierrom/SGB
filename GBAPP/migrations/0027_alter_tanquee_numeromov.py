# Generated by Django 4.2.1 on 2023-07-08 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0026_tanquee_pesainicial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanquee',
            name='NumeroMov',
            field=models.IntegerField(default=5001, primary_key=True, serialize=False, unique=True),
        ),
    ]
