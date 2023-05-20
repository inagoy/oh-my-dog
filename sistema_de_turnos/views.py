from django.shortcuts import render, redirect
from .forms import SacarTurnoForm, HorarioForm
from usuarios_y_perros.models import Perro
from sistema_de_turnos.models import Turno
from sistema_de_turnos.helpers import enviar_mail_turno_aceptado


def sacar_turno(request):
    if request.method == 'POST':
        form = SacarTurnoForm(request.POST)
        if form.is_valid():
            form.save()
            # 'solicitud_turno_exitosa' lo cambié para que ande por ahora
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
        # por algun motivo, no funciona  messages.success("El turno fue aceptado")
        return redirect('ver_turnos_solicitados')


def rechazar_turno(request, nroTurno=None):
    #borrar todo esto
        turno = Turno.objects.get(id=nroTurno)
        turno.estado_turno = "RECH"
        turno.save()
        return redirect('index')

        turno = Turno.objects.get(id=turno_id)
        turno.Estado = ACEPTADO
        t.save()






                