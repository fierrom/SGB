# Generated by Django 4.2.1 on 2023-07-08 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0022_remove_tanqact_estado_remove_tanqact_litrosfull_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TanqAct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LitrosMov', models.IntegerField(default=0)),
                ('MovPrevTanque', models.IntegerField(default=0)),
                ('MovPosTanque', models.IntegerField(default=0)),
                ('MoviTanNum', models.IntegerField(default=0)),
            ],
        ),
    ]
