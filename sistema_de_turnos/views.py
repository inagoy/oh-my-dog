from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AtencionForm, SacarTurnoForm, HorarioForm, SugerenciaForm, InyeccionForm, DesparasitanteForm
from usuarios_y_perros.models import Perro,Usuario
from sistema_de_turnos.models import Turno, Atencion, Inyeccion, Desparasitante
from sistema_de_turnos.helpers import enviar_mail_turno_aceptado, enviar_mail_turno_rechazado, enviar_mail_turno_cancelado


def ver_turnos_del_dia(request):

    def es_hoy(fecha):  # se podría llevar a Turno
        delta = date.today() - fecha
        return delta.days == 0

    turnos_aceptados = Turno.objects.filter(
        estado_turno=Turno.Estado.ACEPTADO).order_by('horario')
    turnos_hoy = [obj for obj in turnos_aceptados if es_hoy(obj.fecha_turno)]
    return render(request, 'sistema_de_turnos/turnos_del_dia.html', {'turnos': turnos_hoy})


def sacar_turno(request):
    if request.method == 'POST':
        form = SacarTurnoForm(request.POST)
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
        if form.is_valid():
            form.save()
            messages.success(request, "Se generó la solicitud de turno")
            return redirect('index')
    else:
        form = SacarTurnoForm()
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    return render(request, 'sistema_de_turnos/sacar_turno.html', {'form': form})


def ver_turnos_solicitados(request):
    turnos = Turno.objects.filter(estado_turno=Turno.Estado.SOLICITADO)
    return render(request, 'sistema_de_turnos/ver_turnos_solicitados.html', {'turnos': turnos})


def aceptar_turno(request, nroTurno=None, horario=None):
    # cambiar el estado a aceptado y guardar
    turno = Turno.objects.get(id=nroTurno)
    turno.estado_turno = "ACEP"
    form = HorarioForm(request.POST)
    horario = request.POST['Horario']
    turno.horario = request.POST['Horario']
    turno.save()
    enviar_mail_turno_aceptado(turno, horario)
    messages.success(request, "El turno fue aceptado")
    return redirect('ver_turnos_solicitados')


def rechazar_turno(request, nroTurno=None, sugerencia=None):
    turno = Turno.objects.get(id=nroTurno)
    turno.estado_turno = "RECH"
    form = SugerenciaForm(request.POST)
    sugerencia = request.POST['Sugerencia']
    turno.sugerencia_turno = sugerencia
    turno.save()
    enviar_mail_turno_rechazado(turno, sugerencia)
    messages.success(request, "El turno fue rechazado")
    return redirect('ver_turnos_solicitados')


def cancelar_turno(request, nroTurno=None):
    turno = Turno.objects.get(id=nroTurno)
    turno.estado_turno = "CANC"
    turno.save()
    enviar_mail_turno_cancelado(turno)
    messages.success(request, "El turno fue cancelado")
    return redirect('ver_turnos_solicitados')


def ver_historia_clinica(request, perro_id):
    perro = Perro.objects.get(id=perro_id)
    atenciones = Atencion.objects.filter(turno__perro=perro)
    context = {
        'perro': perro,
        'atenciones': atenciones
    }
    return render(request, 'sistema_de_turnos/historia_clinica.html', context)

def llenar_libreta_sanitaria(request, nroTurno):
    turno = Turno.objects.get(id=nroTurno)
    if turno.motivo == 'DESP':
        if request.method == 'POST':
            form = DesparasitanteForm(request.POST)
            if form.is_valid():
                desparasitante = form.save(commit=False)
                desparasitante.turno = turno
                desparasitante.save()
                return redirect('index')
        else:
            form = DesparasitanteForm()
    else:
        if request.method == 'POST':
            form = InyeccionForm(request.POST)
            if form.is_valid():
                inyeccion = form.save(commit=False)
                inyeccion.turno = turno
                inyeccion.save()
                return redirect('index')
        else:
            form = InyeccionForm()
    context = {
            'form': form,
            'turno': turno,
        }
    return render(request, 'sistema_de_turnos/llenar_libreta_sanitaria.html', context)

def ver_libreta_sanitaria(request, perro_id):
    perro = Perro.objects.get(id=perro_id)
    inyecciones = Inyeccion.objects.filter(turno__perro=perro)
    desparasitantes = Desparasitante.objects.filter(turno__perro=perro)
    context = {
        'perro': perro,
        'inyecciones': inyecciones,
        'desparasitantes': desparasitantes
    }
    
    return render(request, 'sistema_de_turnos/libreta_sanitaria.html', context)

#se muestran TODOS los turnos del usuario, con todos los estados y todas las fechas
def ver_turnos(request):
    perros = Perro.objects.filter(dueño=request.user, activo=True)
    turnos = []
    for perro in perros:
        turnos = turnos + list(Turno.objects.filter(perro=perro))
    return render(request, 'sistema_de_turnos/ver_turnos.html', {'turnos': turnos})

def ver_proximos_turnos(request):
    perros = Perro.objects.filter(dueño=request.user, activo=True)
    turnos = []
    for perro in perros:
        turnos = turnos + list(Turno.objects.filter(perro=perro, estado_turno='SOLI'))
        turnos = turnos + list(Turno.objects.filter(perro=perro, estado_turno='ACEP'))
    return render(request, 'sistema_de_turnos/ver_proximos_turnos.html', {'turnos': turnos})

def completar_atencion(request, nroTurno):
    turno = Turno.objects.get(id=nroTurno)
    if request.method == 'POST':
        form = AtencionForm(request.POST)
        if form.is_valid():
            form.instance.turno = turno
            user = Usuario.objects.get(id=turno.perro.dueño.pk)
            if form.instance.precio <= user.descuento_atencion:
                form.instance.descuento = form.instance.precio
            else:
                form.instance.descuento = user.descuento_atencion
            form.save()
            user.descuento_atencion = 0
            user.save()
            turno.estado_turno = 'CONC'
            turno.save()
            messages.success(request, 'Atención guardada correctamente.')
            submit_action = request.POST.get('submit_action')
            if submit_action == 'agregar_atencion':
                return redirect('ver_historia_clinica', turno.perro.pk)
            elif submit_action == 'completar_libreta':
                return redirect('llenar_libreta_sanitaria', nroTurno=nroTurno)
    else:
        form = AtencionForm()

    context = {
        'form': form,
        'turno': turno,
    }
    return render(request, 'sistema_de_turnos/completar_atencion.html', context)
