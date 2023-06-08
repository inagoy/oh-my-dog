from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AdopcionForm, TarjetaForm, DonacionForm
from .models import Perro
from publicaciones.models import Adopcion, CampaniaDonacion
from publicaciones.helpers import enviar_mail_contestar_adopcion
from usuarios_y_perros.models import Usuario
from django.core.exceptions import ValidationError


def donar(request, campania_id=None):
    # return redirect("campanias")
    if request.method == 'POST':
        form_donacion = DonacionForm(request.POST)
        form_tarjeta = TarjetaForm(request.POST)
        # raise ValidationError(f'{request.POST["fecha_vencimiento_month"]}')
        if form_donacion.is_valid() and form_tarjeta.is_valid():
            # raise ValidationError(f'{form_tarjeta.cleaned_data["fecha_vencimiento"]}')
            donacion = form_donacion.save(commit=False)
            donacion.campania = CampaniaDonacion.objects.get(id=campania_id)
            donacion.usuario = request.user
            donacion.save()
            messages.success(request, "Se concretó la donación")
            return redirect('index')
    form_donacion = DonacionForm()
    form_tarjeta = TarjetaForm()
    campania = CampaniaDonacion.objects.get(id=campania_id)
    return render(request, 'publicaciones/donar.html', {'form_donacion': form_donacion, 'form_tarjeta': form_tarjeta, 'campania': campania})


def crear_campania(request):
    if request.method == 'POST':
        try:
            CampaniaDonacion.objects.get(nombre=request.POST['Nombre'])
            messages.error(request, "La campaña ingresada ya se encuentra en el sistema")
        except CampaniaDonacion.DoesNotExist:
            campania = CampaniaDonacion.objects.create_campania(request.POST['Nombre'], request.POST['Descripcion'], request.POST['FechaLimite'])
            campania.save()
            messages.success(request, "Se ha creado la campaña de donación")
    return redirect("campanias")


def campanias(request):
    campanias = CampaniaDonacion.objects.all()
    return render(request, 'publicaciones/campanias.html', {'campanias': campanias})


def crear_adopcion(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST)
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
        if form.is_valid():
            perro = form.cleaned_data.get('perro')
            if perro is not None and Adopcion.objects.filter(perro=perro).exists():
                messages.error(
                    request, f"{perro} ya tiene una publicación de Adopción")
                return redirect('crear_adopcion')
            form.instance.usuario = request.user
            form.save()
            messages.success(
                request, "Se ha creado la adopción")
            return redirect('adopciones')
    else:
        form = AdopcionForm()
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    return render(request, 'publicaciones/crear_adopcion.html', {'form': form})


def adopciones(request):
    if request.method == 'POST':
        adopciones = None
    else:
        adopciones = Adopcion.objects.all()
    return render(request, 'publicaciones/adopciones.html', {'adopciones': adopciones})


def contestar_adopcion(request, usuario_id=None, adopcion_id=None):
    if request.method == 'POST':
        mensaje = request.POST['Mensaje']
        adopcion = Adopcion.objects.get(id=adopcion_id)
        nombre_perro = adopcion.nombre
        if request.user.is_authenticated:
            usuario = Usuario.objects.get(id=request.user.id)
            enviar_mail_contestar_adopcion(usuario.email, usuario.nombre, mensaje, nombre_perro)
        else:
            nombre = request.POST['Nombre']
            email = request.POST['Email']
            enviar_mail_contestar_adopcion(email, nombre, mensaje, nombre_perro)
        messages.success(request, "Se envío mail de solicitud de adopción")
        return redirect('adopciones')


def marcar_adopcion_resuelta(request, nroAdopcion=None):
    adopcion = Adopcion.objects.get(id=nroAdopcion)
    adopcion.estado_publicacion = "I"
    if not adopcion.perro == None:
        adopcion.perro.activo = False
    adopcion.save()
    return redirect('adopciones')
