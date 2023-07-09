from django import forms

from usuarios_y_perros.models import Perro
from .models import Tinder


class TinderForm(forms.ModelForm):
    perro = forms.ModelChoiceField(
        label="",
        queryset=Perro.objects.all(),
        empty_label='Seleccione uno de sus perros',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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

    sexo = forms.ChoiceField(choices=[("", ""), ('H', "Hembra"), ('M', "Macho"), ], required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Perro
        fields = ['sexo', 'fecha_ultimo_celo']
