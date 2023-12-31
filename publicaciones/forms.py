from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from usuarios_y_perros.models import Perro
from .models import Adopcion, CampaniaDonacion, Donacion, PerdidoEncontrado, Tarjeta, Raza
from .widgets import MonthYearWidget
from django.core.validators import MinValueValidator


class TarjetaForm(forms.ModelForm):

    class Meta:
        year = int(date.today().year)
        year_digits = range(year, year + 10)
        years = {"": "---"}
        for year in year_digits:
            years[year] = str(year)[2:]
        model = Tarjeta
        fields = ['numero', 'clave', 'fecha_vencimiento', ]
        labels = {
            'numero': 'Número de la tarjeta de crédito',
            'clave': 'Clave de la tarjeta de crédito',
            'fecha_vencimiento': 'Fecha de vencimiento de la tarjeta de crédito (mm/aa)',
        }
        widgets = {
            "numero": forms.NumberInput(attrs={"class": "form-control", "name": "numero", "required": "True", }),
            "clave": forms.NumberInput(attrs={"class": "form-control", "name": "clave", "required": "True", }),
            "fecha_vencimiento": MonthYearWidget(months={"": "---", "01": "01", "02": "02", "03": "03", "04": "04", "05": "05", "06": "06", "07": "07", "08": "08", "09": "09", "10": "10", "11": "11", "12": "12"},
                                                 years=years)
        }

    def clean(self):
        super().clean()
        form_data = self.cleaned_data
        if not Tarjeta.objects.filter(numero=form_data['numero']).exists():
            raise ValidationError(
                'El número de tarjeta ingresado es inválido')
        else:
            tarjeta = Tarjeta.objects.get(numero=form_data['numero'])
            if tarjeta.clave != form_data['clave']:
                raise ValidationError('La clave de la tarjeta es inválida')
            else:
                hoy = date.today()
                if form_data['fecha_vencimiento'].year == hoy.year and form_data['fecha_vencimiento'].month < hoy.month:
                    raise ValidationError("La tarjeta se encuentra vencida")


class DonacionForm(forms.ModelForm):

    class Meta:
        model = Donacion
        fields = ['monto', ]
        labels = {'monto': 'Monto a donar', }
        widgets = {'monto': forms.NumberInput(attrs={
            "class": "form-control",
            "step": 0.01,
            "max": 999999999.99,
            "placeholder": "",
            "name": "monto",
            "required": "True",
        })}


class CampaniaDonacionForm(forms.ModelForm):

    class Meta:
        model = CampaniaDonacion
        fields = ['nombre', 'descripcion', 'fecha_limite']
        labels = {
            'nombre': 'Nombre de la campaña',
            'descripcion': 'Descripción',
            'fecha_limite': 'Último día para donar',
        }
        widgets = {
            "nombre": forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'name': 'nombre'}),
            "descripcion": forms.TextInput(attrs={'class': 'form-control', 'id': 'descripcion', 'name': 'descripcion'}),
            "fecha_limite": forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control', 'id': 'fecha_limite', 'name': 'fecha_limite'}),
        }

    def clean_nombre(self):
        nombre_form = self.cleaned_data['nombre']
        if CampaniaDonacion.objects.filter(nombre=nombre_form).exists():
            raise ValidationError(
                'No se pudo agregar, el nombre de campaña ya existe en el sistema.')
        return nombre_form


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


class PerdidoForm(forms.ModelForm):
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
                   'placeholder': 'aaaa-mm-dd (DOB)', 
                   'class': 'form-control',
                   'id': 'fecha_nacimiento'}
        )
    )
    cuando = forms.DateField(
        label='Cuándo',
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'form-control',
                   'id': 'fecha_perdida'}
        )
    )
    donde = forms.CharField(
        label='Dónde',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    foto = forms.ImageField(
        required=True,
        label='Foto',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    
    raza_choices = [("", "Desconocida")] + list(Raza.choices)
    raza = forms.ChoiceField(
        choices=raza_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    caracteristica = forms.CharField(
        label='Característica distintiva',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_fecha_nacimiento(self):
        fecha_form = self.cleaned_data["fecha_nacimiento"]
        hoy = date.today()
        if fecha_form is not None and fecha_form > hoy:
            raise forms.ValidationError(
                "La fecha elegida no puede ser posterior al día de hoy")
        return fecha_form

    def clean_cuando(self):
        fecha_form = self.cleaned_data["cuando"]
        hoy = date.today()
        if fecha_form is not None and fecha_form > hoy:
            raise forms.ValidationError(
                "La fecha elegida no puede ser posterior al día de hoy")
        return fecha_form

    class Meta:
        model = PerdidoEncontrado
        fields = ['perro', 'nombre', 'fecha_nacimiento',
                  'raza', 'donde', 'cuando', 'caracteristica', 'foto']
        widgets = {'esPerdido': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.esPerdido = True


class EncontradoForm(forms.ModelForm):
    cuando = forms.DateField(
        label='Cuándo',
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'placeholder': 'aaaa-mm-dd (DOB)', 'class': 'form-control',
                   'id': 'fecha_encontrado'}
        )
    )
    donde = forms.CharField(
        label='Dónde',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    foto = forms.ImageField(
        required=True,
        label='Foto',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    raza_choices = [("", "Desconocida")] + list(Raza.choices)
    raza = forms.ChoiceField(
        choices=raza_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    caracteristica = forms.CharField(
        label='Característica distintiva',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    edadAproximada = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        label='Edad Aproximada (en meses)'
    )

    def clean_edadAproximada(self):
        edadAproximada = self.cleaned_data.get('edadAproximada')
        if edadAproximada is not None and edadAproximada < 0:
            raise forms.ValidationError(
                'La edad aproximada no puede ser menor a 0 meses.')
        return edadAproximada

    def clean_cuando(self):
        fecha_form = self.cleaned_data["cuando"]
        hoy = date.today()
        if fecha_form is not None and fecha_form > hoy:
            raise forms.ValidationError(
                "La fecha elegida no puede ser posterior al día de hoy")
        return fecha_form

    class Meta:
        model = PerdidoEncontrado
        fields = ['nombre', 'raza', 'donde', 'cuando',
                  'edadAproximada', 'caracteristica', 'foto']
        widgets = {'esPerdido': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.esPerdido = False
