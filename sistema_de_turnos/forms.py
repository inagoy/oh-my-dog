from django import forms
from .models import Atencion, Turno, Inyeccion, Desparasitante
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import date


def dias(fecha_anterior, fecha_actual): # se podría llevar a Turno
    delta = fecha_actual - fecha_anterior  # https://stackoverflow.com/questions/8258432/days-between-two-dates/8258465#8258465
    return delta.days


def año_transcurrido(fecha_anterior, fecha_actual): # se podría llevar a Turno
    fecha_esperada = date(fecha_anterior.year+1, fecha_anterior.month, fecha_anterior.day)
    return fecha_actual >= fecha_esperada


class SacarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_turno','perro','motivo','franja_horaria']
        widgets = {
            'fecha_turno': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'form-control'}
            )
        }
    
    def clean_perro(self):
        perro_form = self.cleaned_data['perro']
        if Turno.objects.filter(Q(estado_turno="SOLI") | Q(estado_turno="ACEP"), perro=perro_form).exists():
            raise ValidationError("Este perro ya tiene un turno activo")
        return perro_form

    def clean_fecha_turno(self):
        fecha_form = self.cleaned_data["fecha_turno"]
        hoy = date.today()
        if fecha_form < hoy:
            raise ValidationError("La fecha elegida no puede ser anterior al día de hoy")
        return fecha_form

    def clean(self):
        super().clean()
        form_data = self.cleaned_data
        if self.errors:
            return form_data
        perro_form = form_data["perro"]
        # raise ValidationError(f'{form_data} {perro_form.dueño}')
        edad = perro_form.edad_en_meses(form_data['fecha_turno'])
        if form_data["motivo"] == "VACA":
            # VACUNA TIPO A Y EDAD ACTUAL MENOR A 2 MESES
            if edad in (0, 1):
                raise ValidationError("El perro no alcanza la edad mínima para recibir la vacuna")
            else:
                turnos = Turno.objects.filter(perro=perro_form.id, estado_turno="CONC", motivo="VACA")
                cant_turnos = turnos.count()
                if cant_turnos > 0:
                    cumple_año = año_transcurrido(list(turnos.order_by("fecha_turno"))[-1].fecha_turno, form_data["fecha_turno"])  # casteo porque Django no acepta -1, tmb pordría ser order_by("-fecha_turno") para descendente y tomar [0]
                    if cant_turnos == 1:
                        edad = perro_form.edad_en_meses(turnos[0].fecha_turno)
                        # VACUNA TIPO A Y EDAD ENTRE 2 Y 4 MESES EN ÚNICO TURNO ANTERIOR
                        if (edad in (2, 3, 4)) and dias(turnos[0].fecha_turno, form_data["fecha_turno"]) < 21:
                            raise ValidationError("Deben pasar 21 días desde la primera dosis")
                        # VACUNA TIPO A Y EDAD MAYOR A 4 MESES EN ÚNICO TURNO ANTERIOR SIN AÑO CUMPLIDO DESDE EL ÚLTIMO
                        elif edad > 4 and not cumple_año:
                            raise ValidationError("Todavía no se ha cumplido un año desde la anterior dosis")
                    # VACUNA TIPO A Y MÁS DE UN TURNO ANTERIOR SIN AÑO CUMPLIDO DESDE EL ÚLTIMO
                    elif not cumple_año:
                        raise ValidationError("Todavía no se ha cumplido un año desde la anterior dosis")
        if form_data["motivo"] == "VACB":
            if edad < 4:
                raise ValidationError("El perro no alcanza la edad mínima para recibir la vacuna")
            else:
                turnos = Turno.objects.filter(perro=perro_form.id, estado_turno="CONC", motivo="VACB")  # Turno.objects.filter(perro=perro_form, estado_turno="CONC", motivo="VACB")
                cant_turnos = turnos.count()
                if cant_turnos > 0 and not año_transcurrido(list(turnos.order_by("fecha_turno"))[-1].fecha_turno, form_data["fecha_turno"]):  # casteo porque Django no acepta -1, tmb pordría order_by("-fecha-turno") para descendente y tomer [0]
                    raise ValidationError("Todavía no se ha cumplido un año desde la anterior dosis")
        return form_data


class HorarioForm(forms.Form):
    horario = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time',
                   'placeholder': '00:00', 'class': 'form-control'}
        )
    )


class SugerenciaForm(forms.Form):
    sugerencia = forms.CharField(
    )

class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = ['precio', 'observaciones']

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("Precio must be greater than zero.")
        return precio

class InyeccionForm(forms.ModelForm):
    class Meta:
        model = Inyeccion
        fields = ['peso']

class DesparasitanteForm(forms.ModelForm):
    class Meta:
        model = Desparasitante
        fields = ['peso','cantidad_de_desparasitante']
        
