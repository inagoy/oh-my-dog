from django.shortcuts import render
from .forms import SacarTurnoForm

def sacar_turno(request):
    if request.method == 'POST':
        form = SacarTurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('solicitud_turno_exitosa')
    else:
        form = SacarTurnoForm()
    
    return render(request, 'sacar_turno.html', {'form': form})