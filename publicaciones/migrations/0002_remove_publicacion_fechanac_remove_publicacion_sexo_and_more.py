# Generated by Django 4.2 on 2023-05-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='fechaNac',
        ),
        migrations.RemoveField(
            model_name='publicacion',
            name='sexo',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='fecha_nacimiento',
            field=models.DateField(null=True, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='color',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='descripcion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='nombre',
            field=models.CharField(max_length=255, null=True),
        ),
    ]