from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CargarPerroForm, RegistrarUsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuarios_y_perros.models import (Perro, Usuario)
from datetime import date
from usuarios_y_perros.helpers import es_menor_18, generar_contraseña, enviar_mail_bienvenida


def registrar_usuario(request):
    if request.method == "GET":
        form = RegistrarUsuarioForm()
    else:
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            contraseña = generar_contraseña()
            form.instance.set_password(contraseña)
            enviar_mail_bienvenida(form.instance.email, contraseña)
            form.save()
            return redirect('cargar_perro', user_id=form.instance.id)
        # except:
         #   print("-"*100)
          #  messages.error(
           #     request, ("El mail ya está registrado en el sistema"))
    return render(request, "usuarios_y_perros/registrar_usuario.html", {'form': form})


def cargar_perro(request, user_id=None):
    if request.method == 'POST':
        form = CargarPerroForm(request.POST)
        if form.is_valid():
            if user_id == None:
                form.instance.dueño = request.user
            else:
                form.instance.dueño = Usuario.objects.get(pk=user_id)
            form.save()
            messages.success(
                request, "La carga del perro fue exitosa!")
            return redirect('cargar_perro')
    else:
        form = CargarPerroForm()

    return render(request, "usuarios_y_perros/cargar_perro.html", {'form': form})


def carga_exitosa(request):
    return render(request, "usuarios_y_perros/carga_exitosa.html")


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
            messages.error(
                request, ("Alguno de los datos ingresados no es correcto. Inténtelo de nuevo..."))
            return redirect('iniciar_sesion')
    else:
        return render(request, 'usuarios_y_perros/iniciar_sesion.html', {})


def cerrar_sesion(request):
    logout(request)
    messages.success(request, ("Se cerró la sesión"))
    return redirect('index')


def perro(request, perro_id):
    try:
        perro = Perro.objects.get(id=perro_id)
        data = {
            'nombre': perro.nombre,
            'fecha_nacimiento': perro.fecha_nacimiento,
            'color': perro.color,
            'observaciones': perro.observaciones,
            'sexo': perro.sexo,
            'fecha_ultimo_celo': perro.fecha_ultimo_celo,
            'raza': perro.raza,
            'dueño': perro.dueño.id
        }
        return JsonResponse(data)
    except Perro.DoesNotExist:
        return JsonResponse({'error': 'Perro not found'}, status=404)
