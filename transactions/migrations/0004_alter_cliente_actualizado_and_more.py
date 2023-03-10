# Generated by Django 4.1.5 on 2023-02-17 20:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaccion_valor_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='actualizado',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='num_documento',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='actualizado',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
