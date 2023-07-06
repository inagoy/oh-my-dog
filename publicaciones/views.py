import time
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from .forms import AdopcionForm, EncontradoForm, PerdidoForm, TarjetaForm, DonacionForm, CampaniaDonacionForm
from .models import PerdidoEncontrado, Perro, Tarjeta, Postulante, Donacion
from publicaciones.models import Adopcion, CampaniaDonacion
from publicaciones.helpers import enviar_mail_contestar_adopcion
from usuarios_y_perros.models import Usuario
from .tables import CampaniaDonacionTable, CampaniaDonacionFilter, DonacionTable, DonacionFilter


# def campanias_tabla(request):
#     table = CampaniaDonacionTable(CampaniaDonacion.objects.all())
#     return render(request, "publicaciones/campanias_tabla.html", {"table": table})

class FilteredCampaniasTabla(SingleTableMixin, FilterView):
    table_class = CampaniaDonacionTable
    model = CampaniaDonacion
    template_name = "publicaciones/campanias_tabla.html"
    filterset_class = CampaniaDonacionFilter


class FilteredDonacionesTabla(SingleTableMixin, FilterView):
    table_class = DonacionTable
    model = Donacion
    template_name = "publicaciones/donaciones_tabla.html"
    campania = None
    filterset_class = DonacionFilter
    # filter = DonacionFilter(queryset=Donacion.objects.filter(campania=campania_id))
    # table_data = Donacion.objects.filter(campania__nombre="aaaa")

    def get_queryset(self):
        try:
            self.campania = CampaniaDonacion.objects.get(id=self.kwargs.get('campania_id'))
            if self.campania is not None:
                return Donacion.objects.filter(campania__nombre=self.campania.nombre)
        except CampaniaDonacion.DoesNotExist:
            return Donacion.objects.all()

    def campania(self):
        self.campania = CampaniaDonacion.objects.get(id=self.kwargs.get('campania_id'))

    # def get_table_data(self):
    #     self.campania = CampaniaDonacion.objects.get(id=self.kwargs.get('campania_id'))
    #     if self.campania is not None:
    #         return Donacion.objects.filter(campania__nombre=self.campania.nombre)


def agregar_campania(request, ):
    if request.method == 'POST':
        form = CampaniaDonacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se agregó la campaña de donación")
            return redirect("campañas")
    else:
        form = CampaniaDonacionForm()
    return render(request, 'publicaciones/agregar_campania.html', {'form': form})


def postulantes(request, adopcion_id):
    try:
        adopcion = Adopcion.objects.get(id=adopcion_id)
    except Adopcion.DoesNotExist:
        messages.error(
            request, "La adopción a la que intenta acceder no existe")
        return redirect("adopciones")
    postulantes = Postulante.objects.filter(adopcion=adopcion_id)
    return render(request, 'publicaciones/postulantes.html', {'postulantes': postulantes, 'adopcion': adopcion})


def donar(request, campania_id=None):
    try:
        campania = CampaniaDonacion.objects.get(id=campania_id)
    except CampaniaDonacion.DoesNotExist:
        messages.error(
            request, "La campaña a la que intenta acceder no existe")
        return redirect("campañas")
    if request.method == 'POST':
        form_tarjeta = TarjetaForm(request.POST)
        form_donacion = DonacionForm(request.POST)
        time.sleep(6)
        if form_tarjeta.is_valid() and form_donacion.is_valid():
            tarjeta = Tarjeta.objects.get(numero=int(
                form_tarjeta.cleaned_data['numero']))
            if tarjeta.saldo < form_donacion.cleaned_data['monto']:
                form_donacion.add_error(
                    'monto', 'El monto ingresado excede el límite de la tarjeta')
                return render(request, 'publicaciones/donar.html', {'form_donacion': form_donacion, 'form_tarjeta': form_tarjeta, 'campania': campania})
            donacion = form_donacion.save(commit=False)
            donacion.campania = campania
            donacion.usuario = request.user
            donacion.save()
            donacion.campania.actualizar_monto_recaudado(donacion.monto)
            donacion.campania.save()
            donacion.usuario.aplicar_descuento(donacion.monto)
            donacion.usuario.save()
            messages.success(request, "Se concretó la donación")
            return redirect(f"/publicaciones/campañas/donar/{campania.id}")
        return render(request, 'publicaciones/donar.html', {'form_donacion': form_donacion, 'form_tarjeta': form_tarjeta, 'campania': campania})
    else:
        form_donacion = DonacionForm()
        form_tarjeta = TarjetaForm()
    return render(request, 'publicaciones/donar.html', {'form_donacion': form_donacion, 'form_tarjeta': form_tarjeta, 'campania': campania})


# def crear_campania(request):
#     form = CampaniaDonacionForm()
#     if request.method == 'POST':
#         try:
#             CampaniaDonacion.objects.get(nombre=request.POST['nombre'])
#             messages.error(request, "La campaña ingresada ya se encuentra en el sistema")
#         except CampaniaDonacion.DoesNotExist:
#             form = CampaniaDonacionForm(request.POST)
#             if form.is_valid():
#                 campania = CampaniaDonacion.objects.create_campania(form.cleaned_data['nombre'], form.cleaned_data['descripcion'], form.cleaned_data['fecha_limite'])
#                 campania.save()
#                 messages.success(request, "Se ha creado la campaña de donación")
#     return redirect('campanias')


def campanias(request):
    campanias_sin_limite = CampaniaDonacion.objects.filter(
        fecha_limite__isnull=True).order_by("id")
    campanias_con_limite = CampaniaDonacion.objects.filter(
        fecha_limite__isnull=False).order_by("-id")
    campanias_cumplen = [
        obj for obj in campanias_con_limite if obj.dias_restantes() >= 0]
    campanias = list(campanias_sin_limite) + list(campanias_cumplen)
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
            enviar_mail_contestar_adopcion(
                usuario.email, usuario.nombre, mensaje, nombre_perro)
            postulante = Postulante(usuario=usuario, adopcion=adopcion)
            postulante.save()
        else:
            nombre = request.POST['Nombre']
            email = request.POST['Email']
            enviar_mail_contestar_adopcion(
                email, nombre, mensaje, nombre_perro)
            postulante = Postulante(
                nombre=nombre, email=email, adopcion=adopcion)
            postulante.save()
        messages.success(request, "Se envío mail de solicitud de adopción")
        return redirect('adopciones')


def marcar_adopcion_resuelta(request, nroAdopcion=None):
    adopcion = Adopcion.objects.get(id=nroAdopcion)
    adopcion.estado_publicacion = "I"
    if not adopcion.perro == None:
        adopcion.perro.activo = False
    adopcion.save()
    return redirect('adopciones')


def crear_perdido(request):
    if request.method == 'POST':
        form = PerdidoForm(request.POST, request.FILES)
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
        if form.is_valid():
            perro = form.cleaned_data.get('perro')
            if perro is not None and PerdidoEncontrado.objects.filter(perro=perro).exists():
                messages.error(
                    request, f"{perro} ya tiene una publicación de Perdidos")
                return redirect('crear_perdido')
            form.instance.usuario = request.user
            form.save()
            messages.success(
                request, "Se ha creado la publicación de Perdidos")
            return redirect('perdidos_encontrados')
    else:
        form = PerdidoForm()
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    return render(request, 'publicaciones/crear_perdido.html', {'form': form})


def crear_encontrado(request):
    if request.method == 'POST':
        form = EncontradoForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.usuario = request.user
            form.save()
            messages.success(
                request, "Se ha creado la publicación de Perdidos")
            return redirect('perdidos_encontrados')
    else:
        form = EncontradoForm()
    return render(request, 'publicaciones/crear_encontrado.html', {'form': form})


def perdidos_encontrados(request):
    if request.method == 'POST':
        publicaciones = None
    else:
        publicaciones = PerdidoEncontrado.objects.all()
    return render(request, 'publicaciones/perdidos_encontrados.html', {'publicaciones': publicaciones})
