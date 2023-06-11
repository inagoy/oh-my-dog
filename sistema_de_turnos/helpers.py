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

def enviar_mail_turno_rechazado(turno,sugerencia):
    send_mail(
                    "Turno rechazado por ¡Oh my dog!",
                    "Hola! Lamentablemente, no disponemos de un turno para el día solicitado."+
                    "\nTe sugerimos: "+sugerencia+
                    ". Por favor, volvé a solicitar turno para "+ turno.perro.nombre +" teniendo en cuenta "+
                    "nuestra sugerencia o comunicate con la veterinaria. \nSaludos,\nEquipo de ¡Oh my dog!",
                    settings.EMAIL_HOST_USER,
                    ["alive.soluciones.software@gmail.com"],
                    fail_silently=False,
                )

def enviar_mail_turno_cancelado(turno):
    send_mail(
                    "Cancelaste un turno",
                    "Hola! Acabás de cancelar un turno que ya había sido aceptado por ¡Oh my dog!"+
                    "\nEste turno era para el perro "+turno.perro.nombre+
                    ". Podés solicitar un turno para otro momento.",
                    settings.EMAIL_HOST_USER,
                    ["alive.soluciones.software@gmail.com"],
                    fail_silently=False,
                )
