# Generated by Django 4.1.5 on 2023-02-16 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tramite',
            name='valor_total',
        ),
    ]
