# Generated by Django 4.1.5 on 2023-02-14 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_remove_derecho_sale_value_tramitederecho'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaccion',
            name='assessor',
        ),
        migrations.AddField(
            model_name='transaccion',
            name='national_register',
            field=models.CharField(choices=[('rna', 'RNA'), ('rnc', 'RNC')], default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='document_number',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='classification',
            field=models.CharField(choices=[('automobile', 'automóvil'), ('motorcycle', 'moto')], default='automobile', max_length=30),
        ),
    ]
