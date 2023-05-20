from django import forms
from .models import Turno
from django.core.exceptions import ValidationError
from django.db.models import Q


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


class HorarioForm(forms.Form):
    horario = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time',
                   'placeholder': '00:00', 'class': 'form-control'}
        )
    )