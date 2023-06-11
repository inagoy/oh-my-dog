from django.db import models


class Turno(models.Model):
    fecha_turno = models.DateField()
    perro = models.ForeignKey(
        "usuarios_y_perros.Perro", on_delete=models.CASCADE,)
    sugerencia_turno = models.CharField(max_length=50)
    horario = models.TimeField(blank=True, null=True)

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
        VACUNA_TIPOB = "VACB", "Vacunación antirrábica"
        DESPARASITACION = "DESP", "Desparasitación"
        CONSULTA = "CONS", "Consulta general"
        URGENCIA = "URGE", "Urgencia"
        CASTRACION = "CAST", "Castración"

    motivo = models.CharField(
        max_length=4,
        choices=Motivo.choices,
        default=Motivo.CONSULTA,
    )

    # Otra forma de armar choices
    MAÑANA = "TM"
    TARDE = "TT"
    FRANJA_HORARIA_OPCIONES = [
        (MAÑANA, "Mañana"),
        (TARDE, "Tarde"),
        (None, "Seleccione una opción")
    ]
    # default=MAÑANA podría agregarlo
    franja_horaria = models.CharField(
        max_length=2, choices=FRANJA_HORARIA_OPCIONES)

    def dueño(self):
        return self.perro.dueño

    def get_motivo(self):
        return self.Motivo(self.motivo).label

    def get_franja_horaria(self):
        for option in self.FRANJA_HORARIA_OPCIONES:
            if option[0] == self.franja_horaria:
                return option[1]
        return ""

    def __str__(self):
        return f'{self.perro.nombre} {self.fecha_turno}'


class Atencion(models.Model):
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    observaciones = models.TextField(blank=True)


class Inyeccion(models.Model):
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=6, decimal_places=2,)
    
    VACUNA_A = "VACA"
    VACUNA_B = "VACB"
    DESPARASITANTE = "DESP"
    INYECCION_OPCIONES = [
        (VACUNA_A, "Vacuna Tipo A"),
        (VACUNA_B, "Vacuna Tipo B"),
        (DESPARASITANTE, "Desparasitante"),
        (None, "Seleccione una opción")
    ]
    
    tipo_inyeccion = models.CharField(
        max_length=4, choices=INYECCION_OPCIONES)
    
    cantidad_de_desparasitante = models.DecimalField(max_digits=6, decimal_places=2,)

    REQUIRED_FIELDS = ['peso', 'tipo_inyeccion', 'cantidad_de_desparasitante']

