from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from publicaciones.helpers import enviar_mail_contestar_adopcion
from servicio_vinculacion.forms import EditPerroTinderForm, TinderForm
from servicio_vinculacion.helpers import enviar_mail_contestar_tinder
from servicio_vinculacion.models import Tinder
from usuarios_y_perros.models import Perro, Usuario


def deshabilitar_perro_tinder(request, tinder_id=None):
    tinder = Tinder.objects.get(id=tinder_id)
    tinder.estado_tinder = "I"
    tinder.save()
    messages.success(
        request, 'Se eliminó el perfil del perro en el servicio de vinculación')
    return perros_asociados(request)


def perros_asociados(request):
    if request.user.is_staff:
        perros = Tinder.objects.filter(estado_tinder="A")
    else:
        perros = Tinder.objects.filter(perro__dueño=request.user.id) & Tinder.objects.filter(estado_tinder="A")
    return render(request, 'servicio_vinculacion/perros_asociados_tinder.html', {'perros': perros})


def ver_mensaje_concientizacion(request):
    return render(request, 'servicio_vinculacion/concientizacion.html')


def ingresar_servicio_vinculacion(request):
    if request.method == 'POST':
        form = TinderForm(request.POST)
        form.fields['perro'].queryset = Perro.objects.filter(dueño=request.user)
        if form.is_valid():
            selected_perro = form.cleaned_data['perro']
            if selected_perro.edad_meses() < 6:
                messages.error(
                    request, 'El perro seleccionado debe tener más de 6 meses')
                return redirect('ingresar_servicio_vinculacion')
            return redirect('edit_perro_tinder', perro_id=selected_perro.id)
        else:
            perro_id = form.data.get('perro')
            if Tinder.objects.filter(perro=perro_id).exists():
                return redirect('tinder_perro', perro_id=perro_id)
    else:
        form = TinderForm()
        form.fields['perro'].queryset = Perro.objects.filter(dueño=request.user)
    return render(request, 'servicio_vinculacion/vinculacion.html', {'form': form})


def edit_perro_tinder(request, perro_id):

    perro = get_object_or_404(Perro, id=perro_id)
    if request.method == 'POST':
        form = EditPerroTinderForm(request.POST, instance=perro)
        if form.is_valid():
            form.save()
            tinder = Tinder()
            tinder.perro = perro
            tinder.save()
            messages.success(
                request, "La carga del perro al servicio de vinculación fue exitosa!")
            return redirect('tinder_perro', perro_id=perro_id)
        else:
            messages.error(
                request, "No se pudo realizar la carga en el servicio de vinculación")
            return redirect('index')
    else:
        form = EditPerroTinderForm(instance=perro)
    return render(request, "servicio_vinculacion/edit_perro_tinder.html", {'form': form, 'perro': perro})


def paginar(request, elementos, cantidad):
    paginator = Paginator(elementos, cantidad)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def tinder_perro(request, perro_id):
    perro = Perro.objects.get(id=perro_id)
    tinders = Tinder.objects.filter(
        perro__sexo=perro.sexo_opuesto(),
        perro__raza=perro.raza
    ).exclude(
        perro__dueño=request.user,
    ).exclude(
        estado_tinder=Tinder.Estado.INACTIVO,
    )
       
    return render(request, 'servicio_vinculacion/tinder_perro.html',  {'page': paginar(request, tinders, 1), 'perro':perro})


def contestar_tinder(request, perroLiked_id=None, perroLiker_id=None):
    if request.method == 'POST':
        perroLiked = Perro.objects.get(id=perroLiked_id)
        perroLiker = Perro.objects.get(id=perroLiker_id)
        usuario = Usuario.objects.get(id=request.user.id)
        enviar_mail_contestar_tinder(
            usuario.email, usuario.nombre, perroLiker.nombre, perroLiked.nombre)
        messages.success(request, "Se envío mail notificando el Like")
        return redirect('ingresar_servicio_vinculacion')
