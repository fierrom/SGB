# Generated by Django 4.2.1 on 2023-07-08 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0018_tipotanq_alter_tanquem_tipotanque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronograma',
            name='NumPrograma',
            field=models.IntegerField(default=1, primary_key=True, serialize=False, unique=True),
        ),

    ]
