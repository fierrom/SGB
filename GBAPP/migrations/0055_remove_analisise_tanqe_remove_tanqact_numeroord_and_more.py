# Generated by Django 4.2.1 on 2023-07-19 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0054_alter_tanqact_movpostanque_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analisise',
            name='TanqE',
        ),
        migrations.RemoveField(
            model_name='tanqact',
            name='NumeroOrd',
        ),
        migrations.AlterField(
            model_name='tanquee',
            name='NumeroOrden',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='analisise',
            name='TanqE',
            field=models.ManyToManyField(related_name='analisise_numeroo', to='GBAPP.tanquee'),
        ),
        migrations.AddField(
            model_name='tanqact',
            name='NumeroOrd',
            field=models.ManyToManyField(related_name='tanqact_numeroo', to='GBAPP.tanquee'),
        ),
    ]
