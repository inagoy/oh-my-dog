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
                  'raza', 'foto']


class RegistrarUsuarioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y',
                               attrs={'type': 'date',
                                      'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}
                               ))

    class Meta:
        model = Usuario
        fields = ['email', 'nombre',
                  'apellido', 'dni',
                  'fecha_nacimiento', 'domicilio']

    def clean_fecha_nacimiento(self):
        fecha_form = self.cleaned_data["fecha_nacimiento"]
        fecha_actual = date.today()
        fecha = date(fecha_actual.year-18,
                     fecha_actual.month, fecha_actual.day)
        año_min = date(1900, 1, 1)
        if fecha_form > fecha:
            raise ValidationError("El usuario debe ser mayor a 18 años")
        if fecha_form < año_min:
            raise ValidationError(
                "La fecha de nacimiento debe ser posterior al año 1900")
        return fecha_form

    def clean_dni(self):
        dni_form = self.cleaned_data["dni"]
        if dni_form <= 0:
            raise ValidationError(
                "El número de DNI no puede ser un valor negativo")
        return dni_form
