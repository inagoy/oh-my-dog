from django.core.mail import send_mail
from django.conf import settings

def enviar_mail_contactar_trabajador(email, nombre, mensaje, nombre_trabajador, tipo_trabajador, apellido_usuario=""):
    send_mail(
        "Un usuario de ¡Oh my dog! solicita tus servicios",
        escribir_cuerpo_de_mail_a_trabajador(email, nombre, mensaje, nombre_trabajador, tipo_trabajador, apellido_usuario),
        settings.EMAIL_HOST_USER,
        ["alive.soluciones.software@gmail.com"],
        fail_silently=False
    )

def enviar_mail_a_veterinaria_contactar_trabajador(email, nombre, email_trabajador, nombre_trabajador, tipo_trabajador,apellido_usuario=""):
    send_mail(
        "Un usuario de ¡Oh my dog! se contactó con un paseador o cuidador",
        escribir_cuerpo_de_mail_a_veterinaria(email, nombre, email_trabajador, nombre_trabajador, tipo_trabajador, apellido_usuario),
        settings.EMAIL_HOST_USER,
        ["alive.soluciones.software@gmail.com"],
        fail_silently=False
    )

def escribir_cuerpo_de_mail_a_trabajador(email, nombre, mensaje, nombre_trabajador, tipo_trabajador,apellido_usuario=""):
    texto = f"""Hola {nombre_trabajador}, te contamos que {nombre} {apellido_usuario} quiere contactarse con vos para que seas el/la {tipo_trabajador}/a de alguno de sus perros.\n
            El mensaje que envió es el siguiente:\n
            {mensaje}\n
            Para comunicarte, le podés enviar un mail a la siguiente dirección: {email}.\n
            Gracias por confiar en ¡Oh my dog!"""
    return texto

def escribir_cuerpo_de_mail_a_veterinaria(email, nombre, email_trabajador, nombre_trabajador, tipo_trabajador,apellido_usuario=""):
    texto = f"""El usuario con nombre {nombre} {apellido_usuario} y cuyo email es {email} se contactó con {nombre_trabajador} cuyo mail es {email_trabajador} por sus servicios de {tipo_trabajador}"""
    return texto