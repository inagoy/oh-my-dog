from datetime import date
from django import forms
from django.forms import SelectDateWidget
from usuarios_y_perros.models import Perro
from .models import Adopcion, CampaniaDonacion, Donacion, Tarjeta
from .widgets import MonthYearWidget
from django_yearmonth_widget.widgets import DjangoYearMonthWidget


class TarjetaForm(forms.ModelForm):

    class Meta:
        model = Tarjeta
        fields = ['numero', 'clave', 'fecha_vencimiento', ]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control", "name": "Numero", "required": "True", }),
            "clave": forms.NumberInput(attrs={"class": "form-control", "name": "Clave", "required": "True", }),
            "fecha_vencimiento": MonthYearWidget(empty_label="---", months={"None": "---", "01": "01", "02": "02", "03": "03", "04": "04", "05": "05", "06": "06", "07": "07", "08": "08", "09": "09", "10": "10", "11": "11", "12": "12"}),
        }


class DonacionForm(forms.ModelForm):
    monto = forms.DecimalField(widget=forms.NumberInput(attrs={
                "class": "form-control",
                "step": 0.01,
                "placeholder": "",
                "name": "Monto",
                "required": "True",
            }))

    class Meta:
        model = Donacion
        fields = ['monto', ]


class CampaniaDonacionForm(forms.ModelForm):

    class Meta:
        model = CampaniaDonacion
        fields = ['nombre', 'descripcion', 'fecha_limite']
        widgets = {
            "fecha_limite": forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'date', })
        }


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
