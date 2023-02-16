# Generated by Django 4.1.5 on 2023-02-16 16:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('tipo_documento', models.CharField(choices=[('CC', 'Cedula de Ciudadania'), ('CE', 'Cedula de Extranjeria'), ('TI', 'Tarjeta de Identidad'), ('RC', 'Registro Civil'), ('PA', 'Pasaporte')], default='CC', max_length=2)),
                ('num_documento', models.CharField(max_length=20)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Derecho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('registro', models.CharField(choices=[('RNA', 'Registro Nacional de Automotores'), ('RNC', 'Registro Nacional de Conductor')], default='RNA', max_length=3)),
                ('clasificacion', models.CharField(choices=[('MOTO', 'Moto'), ('AUTOMOVIL', 'Automovil'), ('MOTOCARRO', 'Motocarro')], default='AUTOMOVIL', max_length=50)),
                ('vigencia', models.DateField()),
                ('valor_total', models.DecimalField(decimal_places=0, default=0.0, max_digits=10)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_vehiculo', models.CharField(choices=[('MOTO', 'Moto'), ('AUTOMOVIL', 'Automovil'), ('MOTOCARRO', 'Motocarro')], default='AUTOMOVIL', max_length=50)),
                ('placa', models.CharField(max_length=20)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PAGADO', 'Pagado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', max_length=10)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.cliente')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.tramite')),
                ('vehiculo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='TramiteDerecho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=0, max_digits=10)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(default=django.utils.timezone.now)),
                ('derecho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.derecho')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.tramite')),
            ],
        ),
        migrations.AddField(
            model_name='tramite',
            name='derechos',
            field=models.ManyToManyField(related_name='derechos', through='transactions.TramiteDerecho', to='transactions.derecho'),
        ),
    ]
