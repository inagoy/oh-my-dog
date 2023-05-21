from django import forms
from usuarios_y_perros.models import Perro
from .models import Adopcion


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
    
    class Meta:
        model = Adopcion
        fields = ['perro', 'descripcion', 'nombre',
                  'fecha_nacimiento', 'color', 'raza']
