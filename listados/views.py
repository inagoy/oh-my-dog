from django.shortcuts import render, redirect

from listados.filters import PaseadoresCuidadoresFilter
from listados.models import Trabajador
from .forms import CargarTrabajadorForm
from publicaciones.models import CampaniaDonacion
from django.contrib import messages
from usuarios_y_perros.models import Usuario
from listados.helpers import enviar_mail_contactar_trabajador, enviar_mail_a_veterinaria_contactar_trabajador

def paseadores_cuidadores(request):
    campanias_sin_limite = CampaniaDonacion.objects.filter(
        fecha_limite__isnull=True).order_by("id")
    campanias_con_limite = CampaniaDonacion.objects.filter(
        fecha_limite__isnull=False).order_by("-id")
    campanias_cumplen = [
        obj for obj in campanias_con_limite if obj.dias_restantes() >= 0]
    servicios = list(campanias_sin_limite) + list(campanias_cumplen)

    filtro = PaseadoresCuidadoresFilter(request.GET, queryset=Trabajador.objects.all())
    return render(request, 'listados/paseadores_cuidadores.html', {'servicios': servicios, 'filtro': filtro})


def cargar_trabajador(request):
    if request.method == "GET":
        form = CargarTrabajadorForm()
    else:
        form = CargarTrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La carga del paseador o cuidador fue exitosa")
            return redirect('index')
    return render(request, 'listados/cargar_trabajador.html',{'form': form})

def deshabilitar_trabajador(request):
    return render(request,'index')

def contactar_trabajador(request, trabajador_id=None):
    if request.method == 'POST':
        mensaje = request.POST['Mensaje']
        trabajador = Trabajador.objects.get(id=trabajador_id)

        nombre_trabajador = trabajador.nombre_y_apellido
        tipo_trabajador = trabajador.get_tipo_display().lower()
        email_trabajador = trabajador.email

        if request.user.is_authenticated:
            usuario = Usuario.objects.get(id=request.user.id)
            enviar_mail_contactar_trabajador(
                usuario.email, usuario.nombre, mensaje, nombre_trabajador, tipo_trabajador, usuario.apellido
            )
            enviar_mail_a_veterinaria_contactar_trabajador(
                usuario.email, usuario.nombre, email_trabajador, nombre_trabajador, tipo_trabajador,usuario.apellido
            )
        else:
            nombre = request.POST['Nombre']
            email = request.POST['Email']
            enviar_mail_contactar_trabajador(
                email, nombre, mensaje, nombre_trabajador, tipo_trabajador
            )
            enviar_mail_a_veterinaria_contactar_trabajador(
                
                email, nombre, email_trabajador, nombre_trabajador, tipo_trabajador
            )

        messages.success(request, "Se envió el mail al/la "+tipo_trabajador+"/a para que se puedan poner en contacto")
        return redirect('paseadores_cuidadores')