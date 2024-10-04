from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.utils import timezone

from apps.anuncio.models import Anuncio


class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ('titulo', 'descripcion', 'precio_inicial', 'imagen', 'fecha_inicio', 'categorias')

        widgets = {
            'imagen': forms.ClearableFileInput(),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio < timezone.now():
            raise ValidationError('La Fecha de Inicio de la Subasta debe ser igual o posterior a la Fecha Actual')
        return fecha_inicio


class AnuncioModificaForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ('titulo', 'descripcion', 'imagen', 'fecha_inicio', 'categorias')

        widgets = {
            'imagen': forms.ClearableFileInput(),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'
