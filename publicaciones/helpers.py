from django.core.mail import send_mail
from django.conf import settings

def enviar_mail_contestar_adopcion(mail, nombre, mensaje):
    send_mail(
                    "Solicitud de adopción en ¡Oh my dog!",
                    nombre + " quiere adoptar a tu perro " + "publicado en ¡Oh my dog!. "
                    "Si estás interesadx, escribile a su mail " + mail + "." +
                    "\nSi concretan la adopción recordá que podés cerrar la publicación para no recibir más respuestas."
                    "\nSaludos,\nEquipo de ¡Oh my dog!",
                    settings.EMAIL_HOST_USER,
                    ["alive.soluciones.software@gmail.com"],
                    fail_silently=False,
                )