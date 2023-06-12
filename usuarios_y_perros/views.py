import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
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
        form = CargarPerroForm(request.POST, request.FILES)
        if form.is_valid():
            if user_id == None:
                form.instance.dueño = request.user
            else:
                form.instance.dueño = Usuario.objects.get(pk=user_id)

            nombre_perro = form.cleaned_data['nombre']
            if Perro.objects.filter(dueño=form.instance.dueño, nombre=nombre_perro).exists():
                if user_id == None:
                    messages.error(
                        request, "Ya tenes un perro con este nombre.")
                    return redirect('cargar_perro')
                else:
                    messages.error(
                        request, "El usuario  ya tiene un perro con este nombre")
                    return redirect('cargar_perro', user_id)
            form.save()
            messages.success(
                request, "La carga del perro fue exitosa!")
            if user_id == None:
                return redirect('cargar_perro')
            else:
                return redirect('cargar_perro', user_id)
    else:
        form = CargarPerroForm()

    return render(request, "usuarios_y_perros/cargar_perro.html", {'form': form})


def iniciar_sesion(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Te damos la bienvenida a ¡Oh my dog!")
            return redirect('index')
        else:
            try:
                Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                messages.error(
                    request, "El mail ingresado no se encuentra registrado en el sistema")
            else:
                messages.error(request, "La contraseña es inválida")
            return redirect('iniciar_sesion')
    else:
        return render(request, 'usuarios_y_perros/iniciar_sesion.html')


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Se cerró la sesión")
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


def ver_perros(request):
    return render(request, 'usuarios_y_perros/ver_perros.html', {
        'perros': Perro.objects.filter(dueño=request.user, activo=True)
    })


def ver_perro(request, perro_id):
    perro = get_object_or_404(Perro, id=perro_id)
    if (perro.dueño == request.user) or request.user.is_staff:
        return render(request, 'usuarios_y_perros/ver_perro.html', {'perro': perro})
    else:
        messages.error(request, "No sos dueño de este perro.")
        return render(request, 'usuarios_y_perros/ver_perros.html', {
            'perros': Perro.objects.filter(dueño=request.user, activo=True)
        })


def ver_perros_como_admin(request, usuario_id):
    return render(request, 'usuarios_y_perros/ver_perros.html', {
        'perros': Perro.objects.filter(dueño=usuario_id, activo=True)
    })


def ver_usuarios_como_admin(request):
    if request.method == 'POST':
        usuarios = None
    else:
        usuarios = Usuario.objects.all()
    return render(request, 'usuarios_y_perros/ver_usuarios_como_admin.html', {
        'usuarios': usuarios
    })


def edit_perro(request, perro_id):

    perro = get_object_or_404(Perro, id=perro_id)
    print(perro.foto, '1')
    if request.method == 'POST':
        form = CargarPerroForm(request.POST, request.FILES, instance=perro)
        if form.is_valid():
            form.save()
            return render(request, 'usuarios_y_perros/ver_perro.html', {'perro': perro})
    else:
        perro.fecha_nacimiento = perro.fecha_nacimiento.strftime('%Y-%m-%d')
        form = CargarPerroForm(instance=perro)
    return render(request, "usuarios_y_perros/editar_perro.html", {'form': form, 'perro': perro})
