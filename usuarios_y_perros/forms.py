from django import forms
from .models import Perro, Usuario
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models import Q
from oh_my_dog import settings

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


class RegistrarUsuarioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
            widget=forms.DateInput(format = '%d/%m/%Y',
            attrs={'type': 'date',
                    'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}
            ),
            input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 
                    'apellido', 'dni', 
                    'fecha_nacimiento', 'domicilio']
    
    def clean_fecha_nacimiento(self):
        fecha_form = self.cleaned_data["fecha_nacimiento"]
        fecha_actual = date.today()
        fecha = date(fecha_actual.year-18, fecha_actual.month, fecha_actual.day)
        if fecha_form > fecha:
            raise ValidationError("El usuario debe ser mayor a 18 años")
        return fecha_form