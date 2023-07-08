from django.core.mail import send_mail
from django.conf import settings


def enviar_mail_contestar_adopcion(mail, nombre, mensaje, perro):
    texto_mensaje = f'Te dejó este mensaje de presentación: {mensaje}' if mensaje  else ""
    send_mail(
        "Solicitud de adopción en ¡Oh my dog!",
        f'{nombre} quiere adoptar al perro {perro} de tu publicación en ¡Oh my dog!. {texto_mensaje}'
        f'\nPodés escribirle a su mail {mail} para continuar el proceso de adopción.'
        f'\nSi concretan la adopción recordá cerrar la publicación para no recibir más respuestas. '
        f'\nSaludos,\nEquipo de ¡Oh my dog!',
        settings.EMAIL_HOST_USER,
        ["alive.soluciones.software@gmail.com"],
        fail_silently=False,
        )

def enviar_mail_contestar_publicacion(mail, nombre, mensaje, perro, esPerdido):
    send_mail(
        "Una persona contestó tu publicación en ¡Oh my dog!",
        generar_texto_mail(mail, nombre, mensaje, perro, esPerdido),
        settings.EMAIL_HOST_USER,
        ["alive.soluciones.software@gmail.com"],
        fail_silently=False,
        )


def generar_texto_mail(email, nombre, mensaje, perro, esPerdido):
    texto_introduccion = f"Te contamos que {nombre} quiere contactarse con vos debido a que cree "

    if esPerdido:
        texto_motivo = f"que encontró a tu perro {perro}."
    else:
        texto_motivo = f"que el perro que publicaste es suyo."
    
    texto_mensaje = f'\nTe dejó este mensaje: {mensaje}' if mensaje  else ""
    texto_fin = f"""\nPara comunicarte, le podés enviar un mail a la siguiente dirección: {email}.\n
            Gracias por confiar en ¡Oh my dog!"""
    return texto_introduccion + texto_motivo + texto_mensaje + texto_fin

