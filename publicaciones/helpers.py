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
