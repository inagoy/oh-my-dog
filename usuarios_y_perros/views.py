from django.shortcuts import render, redirect
from .forms import CargarPerroForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def iniciar_sesion(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Bienvenidx!"))
            return redirect('index')
        else:
            messages.error(request, ("Alguno de los datos ingresados no es correcto. Inténtelo de nuevo..."))	
            return redirect('iniciar_sesion')
    else:
        return render(request, 'usuarios_y_perros/iniciar_sesion.html', {})

def cerrar_sesion(request):
    logout(request)
    messages.success(request, ("Se cerró la sesión"))
    return redirect('index')