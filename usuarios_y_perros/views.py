from django.shortcuts import render, redirect
from .forms import CargarPerroForm

def cargar_perro(request):
    if request.method == 'POST':
        form = CargarPerroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carga_exitosa')
    else:
        form = CargarPerroForm()
    
    return render(request, 'cargar_perro.html', {'form': form})

def carga_exitosa(request):
    return render(request, "carga_exitosa.html")