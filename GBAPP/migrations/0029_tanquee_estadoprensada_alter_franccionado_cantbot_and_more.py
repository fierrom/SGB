# Generated by Django 4.2.1 on 2023-07-09 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GBAPP', '0028_alter_tanquee_numeromov'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanquee',
            name='EstadoPrensada',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='franccionado',
            name='CantBot',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='franccionado',
            name='NumEmbo',
            field=models.IntegerField(default=0),
        ),
    ]
