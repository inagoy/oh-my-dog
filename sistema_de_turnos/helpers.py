from django.core.mail import send_mail
from django.conf import settings

def enviar_mail_turno_aceptado(turno,horario):
    send_mail(
                    "Turno aceptado por ¡Oh my dog!",
                    "Hola! Tu solicitud de turno para "+turno.perro.nombre +" fue aceptada." 
                    ". \nEl turno fue agendado para el día "+turno.fecha_turno.strftime("%d/%m/%Y")+
                    " a las "+ horario,
                    settings.EMAIL_HOST_USER,
                    ["alive.soluciones.software@gmail.com"],
                    fail_silently=False,
                )