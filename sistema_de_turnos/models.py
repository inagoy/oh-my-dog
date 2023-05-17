from django.db import models


class Turno(models.Model):
    fecha_turno = models.DateField()
    perro = models.ForeignKey("usuarios_y_perros.Perro", on_delete=models.CASCADE,)
    sugerencia_turno = models.CharField(max_length=50)

    class Estado(models.TextChoices):
        SOLICITADO = "SOLI", "Solicitado"
        ACEPTADO = "ACEP", "Aceptado"
        RECHAZADO = "RECH", "Rechazado"
        CANCELADO = "CANC", "Cancelado"
        CONCRETADO = "CONC", "Concretado"

    estado_turno = models.CharField(
        max_length=4,
        choices=Estado.choices,
        default=Estado.SOLICITADO,
    )

    class Motivo(models.TextChoices):
        VACUNA_TIPOA = "VACA", "Vacunación para enfermedades"
        VACUNA_TIPOB = "VACB", "Vacunación antiirrábica"
        DESPARASITACION = "DESP", "Desparasitación"
        CONSULTA = "CONS", "Consulta general"
        URGENCIA = "URGE", "Urgencia"

    motivo = models.CharField(
        max_length=4,
        choices=Motivo.choices,
        default=Motivo.CONSULTA,
    )

    #Otra forma de armar choices
    MAÑANA = "TM"
    TARDE = "TT"
    FRANJA_HORARIA_OPCIONES = [
        (MAÑANA, "Mañana"),
        (TARDE, "Tarde"),
        (None, "Seleccione una opción")
    ]
    franja_horaria = models.CharField(max_length=2, choices=FRANJA_HORARIA_OPCIONES) # default=MAÑANA podría agregarlo

    def __str__(self):
        return f'{self.perro.nombre} {self.fecha_turno}'