# Generated by Django 4.2 on 2023-07-02 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios_y_perros', '0005_alter_perro_raza'),
        ('publicaciones', '0009_postulante'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerdidoEncontrado',
            fields=[
                ('publicacion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publicaciones.publicacion')),
                ('esPerdido', models.BooleanField()),
                ('donde', models.CharField(max_length=255, verbose_name='Dónde')),
                ('cuando', models.DateField(verbose_name='Cuándo')),
                ('edadAproximada', models.IntegerField(blank=True, null=True, verbose_name='Edad Aproximada')),
                ('caracteristica', models.CharField(blank=True, max_length=255, null=True, verbose_name='Característica distintiva')),
                ('perro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios_y_perros.perro')),
            ],
            bases=('publicaciones.publicacion',),
        ),
    ]
