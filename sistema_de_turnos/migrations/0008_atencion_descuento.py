# Generated by Django 4.2 on 2023-06-12 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_de_turnos', '0007_merge_20230611_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='atencion',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Descuento'),
        ),
    ]