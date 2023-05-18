from django import forms
from .models import Perro

class CargarPerroForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ['nombre','fecha_nacimiento', 'color', 
                  'observaciones',
                  'raza', 'dueño'] 
