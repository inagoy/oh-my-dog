from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AdopcionForm
from .models import Perro
from publicaciones.models import Adopcion
from publicaciones.helpers import enviar_mail_contestar_adopcion
from usuarios_y_perros.models import Usuario


def crear_adopcion(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST)
        if form.is_valid():
            perro = form.cleaned_data.get('perro')
            if perro is not None and Adopcion.objects.filter(perro=perro).exists():
                messages.error(
                    request, f"{perro} ya tiene una publicación de Adopción")
                return redirect('crear_adopcion')
            form.instance.usuario = request.user
            form.save()
            return redirect('index')
    else:
        form = AdopcionForm()
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    return render(request, 'publicaciones/crear_adopcion.html', {'form': form})


def adopciones(request):
    adopciones = Adopcion.objects.all()
    return render(request, 'publicaciones/adopciones.html', {'adopciones': adopciones})


def contestar_adopcion(request, usuario_id=None):
    if request.method == 'POST':
        mensaje = request.POST['Mensaje']
<<<<<<< HEAD
        if request.user.is_authenticated:
            usuario = Usuario.objects.get(id=request.user.id)
            enviar_mail_contestar_adopcion(usuario.email, usuario.nombre, mensaje)
        else:
            nombre = request.POST['Nombre']
            email = request.POST['Email']
            enviar_mail_contestar_adopcion(email, nombre, mensaje)


=======
        if usuario_id:
            usuario = Usuario.objects.get(id=usuario_id)
            enviar_mail_contestar_adopcion(
                usuario.email, usuario.nombre, mensaje)
>>>>>>> 9489185a9dad6aadcf3ae1f4072bf846438343d1
        # messages.success("Se envío mail de solicitud de adopción")
        return redirect('adopciones')
