from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SacarTurnoForm, HorarioForm, SugerenciaForm
from usuarios_y_perros.models import Perro
from sistema_de_turnos.models import Turno
from sistema_de_turnos.helpers import enviar_mail_turno_aceptado, enviar_mail_turno_rechazado


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
        #cambiar el estado a aceptado y guardar
        turno = Turno.objects.get(id=nroTurno)
        turno.estado_turno = "ACEP"
        form = HorarioForm(request.POST)
        horario = request.POST['Horario']
        turno.save()
        enviar_mail_turno_aceptado(turno, horario)
        messages.success(request, "El turno fue aceptado")
        return redirect('ver_turnos_solicitados')


def rechazar_turno(request, nroTurno=None, sugerencia=None):
        turno = Turno.objects.get(id=nroTurno)
        turno.estado_turno = "RECH"
        form = SugerenciaForm(request.POST)
        sugerencia = request.POST['Sugerencia']
        turno.save()
        enviar_mail_turno_rechazado(turno, sugerencia)
        messages.success(request, "El turno fue rechazado")
        return redirect('ver_turnos_solicitados')

def ver_turnos(request):
    form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    
    turnos = Turno.objects.filter(perro=request.user)
    return render(request, 'sistema_de_turnos/ver_turnos.html', {'turnos': turnos})





                