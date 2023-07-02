from django.core.mail import send_mail
from django.conf import settings


def enviar_mail_contestar_tinder(mail, postulante, perroLiker, perroLiked):
    send_mail(
        "Notificación del Servicio de Vinculación de ¡Oh my dog!",
        f'{perroLiked} ha recibido un Like de {perroLiker} en ¡Oh my dog!.'
        f'\nPodés escribirle a {postulante} a su mail {mail} si te intereza establecer un vínculo.'
        f'\nRecordá "desvincular" a {perroLiked} si deseás que no aparezca más en el Servicio de Vinculación. '
        f'\nSaludos,\nEquipo de ¡Oh my dog!',
        settings.EMAIL_HOST_USER,
        ["alive.soluciones.software@gmail.com"],
        fail_silently=False,
        )
