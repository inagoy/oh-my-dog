# Generated by Django 4.2 on 2023-06-11 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_de_turnos', '0004_turno_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='motivo',
            field=models.CharField(choices=[('VACA', 'Vacunación para enfermedades'), ('VACB', 'Vacunación antirrábica'), ('DESP', 'Desparasitación'), ('CONS', 'Consulta general'), ('URGE', 'Urgencia'), ('CAST', 'Castración')], default='CONS', max_length=4),
        ),
        migrations.CreateModel(
            name='Inyeccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tipo_inyeccion', models.CharField(choices=[('VACA', 'Vacuna Tipo A'), ('VACB', 'Vacuna Tipo B'), ('DESP', 'Desparasitante'), (None, 'Seleccione una opción')], max_length=4)),
                ('cantidad_de_desparasitante', models.DecimalField(decimal_places=2, max_digits=6)),
                ('turno', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sistema_de_turnos.turno')),
            ],
        ),
    ]
