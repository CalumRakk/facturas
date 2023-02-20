# Generated by Django 4.1.5 on 2023-02-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_remove_tramite_valor_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='valor_total',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=10),
        ),
    ]