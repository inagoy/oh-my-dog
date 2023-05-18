from django.shortcuts import render

def solicitar_turno(request):
    return render(request, 'sistema_de_turnos/sacar_turno.html', {})