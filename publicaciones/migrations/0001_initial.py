# Generated by Django 4.2 on 2023-05-19 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios_y_perros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('fechaNac', models.DateField(blank=True, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('sexo', models.CharField(blank=True, max_length=255, null=True)),
                ('estado_publicacion', models.CharField(choices=[('A', 'Activa'), ('I', 'Inactiva')], default='A', max_length=4)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Adopcion',
            fields=[
                ('publicacion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publicaciones.publicacion')),
                ('perro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios_y_perros.perro')),
            ],
            bases=('publicaciones.publicacion',),
        ),
    ]
