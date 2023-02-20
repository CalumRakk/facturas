# Generated by Django 4.1.5 on 2023-02-18 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_transaccion_vehiculo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tramite',
            unique_together={('nombre', 'registro', 'clasificacion', 'vigencia')},
        ),
    ]
