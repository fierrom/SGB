# Generated by Django 4.2.1 on 2023-07-10 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0035_remove_tanqact_movitannum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analisise',
            name='TanqE',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GBAPP.tanquee', to_field='NumeroOrden'),
            preserve_default=False,
        ),
    ]