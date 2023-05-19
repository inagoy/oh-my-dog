from django import forms
from .models import Perro


class CargarPerroForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'form-control'}
        )
    )

    class Meta:
        model = Perro
        fields = ['nombre', 'fecha_nacimiento', 'color',
                  'observaciones',
                  'raza']
