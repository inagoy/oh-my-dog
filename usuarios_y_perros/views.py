from django.shortcuts import render, redirect
from .forms import CargarPerroForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuarios_y_perros.models import (Usuario)
from datetime import date
from usuarios_y_perros.helpers import es_menor_18, generarContraseña
from django.core.mail import send_mail
from django.conf import settings

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

def registrar_usuario(request):
    if request.method == "GET":
        return render(request,"usuarios_y_perros/registrar_usuario.html")
    elif request.method == "POST":
        u = Usuario()
        u.email = request.POST['email']
        u.nombre = request.POST['nombre']
        u.apellido = request.POST['apellido']
        u.fechaNacimiento = date.fromisoformat(request.POST['fechaNacimiento'])
        u.dni = request.POST['dni']
        u.direccion = request.POST['direccion']
        u.set_password = generarContraseña()
        if (es_menor_18(u.fechaNacimiento)):
            messages.error(request, "El usuario es menor de edad y no puede ser usuario del sistema")
            return redirect('registrar_usuario')
        try:
            u.save()
            send_mail(
                "Bienvenidx a ¡Oh my dog!",
                "Acá va un mensaje lindo",
                settings.EMAIL_HOST_USER,
                ["alive.soluciones.software@gmail.com"],
                fail_silently=False,
            )
            print("INFO: Email enviado a: "+u.email)
        except:
            print("-"*100)
            messages.error(request, ("El mail ya está registrado en el sistema"))
        return redirect('cargar_perro')
    return redirect('registrar_usuario')

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