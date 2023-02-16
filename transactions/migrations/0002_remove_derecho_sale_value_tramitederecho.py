# Generated by Django 4.1.5 on 2023-02-14 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='derecho',
            name='sale_value',
        ),
        migrations.CreateModel(
            name='TramiteDerecho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('vigencia', models.DateTimeField()),
                ('derecho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.derecho')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.tramite')),
            ],
        ),
    ]
