# Generated by Django 4.2 on 2023-06-12 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_de_turnos', '0007_merge_20230611_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inyeccion',
            name='cantidad_de_desparasitante',
        ),
        migrations.RemoveField(
            model_name='inyeccion',
            name='tipo_inyeccion',
        ),
        migrations.CreateModel(
            name='Desparasitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cantidad_de_desparasitante', models.DecimalField(decimal_places=2, max_digits=6)),
                ('turno', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sistema_de_turnos.turno')),
            ],
        ),
    ]