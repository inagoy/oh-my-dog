from django import forms
from .models import Turno

class SacarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_turno','perro','motivo','franja_horaria']
        widgets = {
            'fecha_turno': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'form-control'}
            )
        }
