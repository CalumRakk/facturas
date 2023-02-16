# Generated by Django 4.1.5 on 2023-02-15 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_cliente_document_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculo',
            name='vehicle_type',
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='classification',
            field=models.CharField(choices=[('automobile', 'automóvil'), ('motorcycle', 'moto')], default='automobile', max_length=30),
        ),
    ]
