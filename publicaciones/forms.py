from datetime import date
from django import forms
from usuarios_y_perros.models import Perro
from .models import Adopcion, CampaniaDonacion


class CampaniaDonacionForm(forms.ModelForm):
    fecha_limite = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date',
                                                                                    'placeholder': 'dd-mm-yyyy (DOB)',
                                                                                    'class': 'form-control'}))

    class Meta:
        model = CampaniaDonacion
        fields = ['nombre', 'descripcion', 'fecha_limite']


class AdopcionForm(forms.ModelForm):
    perro = forms.ModelChoiceField(
        queryset=Perro.objects.all(),
        required=False,
        empty_label='Perro no registrado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'date'}
        )
    )
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    color = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    def clean_fecha_nacimiento(self):
        fecha_form = self.cleaned_data["fecha_nacimiento"]
        hoy = date.today()
        if fecha_form is not None and fecha_form > hoy:
            raise forms.ValidationError(
                "La fecha elegida no puede ser posterior al día de hoy")
        return fecha_form

    class Meta:
        model = Adopcion
        fields = ['perro', 'descripcion', 'nombre',
                  'fecha_nacimiento', 'color', 'raza']
