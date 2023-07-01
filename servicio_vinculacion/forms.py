from django import forms

from usuarios_y_perros.models import Perro
from .models import Tinder


class TinderForm(forms.ModelForm):
    class Meta:
        model = Tinder
        fields = ['perro']

class EditPerroTinderForm(forms.ModelForm):
    fecha_ultimo_celo = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'form-control'}
        )
    )
    class Meta:
        model = Perro
        fields = ['sexo', 'fecha_ultimo_celo']