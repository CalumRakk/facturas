# Generated by Django 4.1.5 on 2023-02-17 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_cliente_num_documento_alter_vehiculo_placa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='vehiculo',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='transactions.vehiculo'),
            preserve_default=False,
        ),
    ]
