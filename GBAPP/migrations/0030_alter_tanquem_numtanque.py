# Generated by Django 4.2.1 on 2023-07-09 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0029_tanquee_estadoprensada_alter_franccionado_cantbot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanquem',
            name='NumTanque',
            field=models.AutoField(default=500, primary_key=True, serialize=False, unique=True),
        ),
    ]