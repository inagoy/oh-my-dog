# Generated by Django 4.2 on 2023-06-10 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_de_turnos', '0003_atencion'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='horario',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
