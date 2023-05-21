from django.shortcuts import render, redirect
from .forms import AdopcionForm
from .models import Perro
from publicaciones.models import Adopcion, Publicacion
from sistema_de_turnos.models import Turno


def crear_adopcion(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST)
        if form.is_valid():
            form.instance.usuario = request.user
            form.save()
            return redirect('index')
    else:
        form = AdopcionForm()
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    return render(request, 'publicaciones/crear_adopcion.html', {'form': form})


def adopciones(request):
    return render(request, 'publicaciones/adopciones.html')

def ver_perros_en_adopcion(request):
    adopciones = Adopcion.objects.filter(estado_publicacion=Adopcion.Estado.ACTIVA)
    return render(request, 'publicaciones/ver_perros_en_adopcion.html', {'adopciones': adopciones})
