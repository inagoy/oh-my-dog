from distutils.errors import PreprocessError
from operator import is_not
from django.shortcuts import render, redirect
from .forms import SacarTurnoForm
from usuarios_y_perros.models import Perro

def sacar_turno(request):
    if request.method == 'POST':
        form = SacarTurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # 'solicitud_turno_exitosa' lo cambié para que ande por ahora
    else:
        form = SacarTurnoForm()
        form.fields["perro"].queryset = Perro.objects.filter(dueño=request.user, activo=True)
    return render(request, 'sacar_turno.html', {'form': form})
