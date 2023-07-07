from django import forms
from .models import Trabajador
from oh_my_dog import settings

class CargarTrabajadorForm(forms.ModelForm):

    class Meta:
        model = Trabajador
        fields = ['nombre_y_apellido', 'zona', 'tipo']



