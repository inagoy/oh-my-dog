# Generated by Django 4.2 on 2023-07-02 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0011_publicacion_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perdidoencontrado',
            name='edadAproximada',
            field=models.IntegerField(blank=True, null=True, verbose_name='Edad Aproximada (en meses)'),
        ),
    ]