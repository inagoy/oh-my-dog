from django.shortcuts import render, redirect
from .forms import SacarTurnoForm
from usuarios_y_perros.models import Perro
from sistema_de_turnos.models import Turno


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
