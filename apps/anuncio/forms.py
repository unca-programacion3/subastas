from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.utils import timezone

from apps.anuncio.models import Anuncio, OfertaAnuncio


class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ('titulo', 'descripcion', 'precio_inicial', 'imagen', 'fecha_inicio', 'categorias')

        widgets = {
            'imagen': forms.ClearableFileInput(),
            'fecha_inicio': DateInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local'}),
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
            'fecha_inicio': DateInput(format='%Y-%m-%d %H:%m', attrs={'type': 'datetime-local'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


# class OfertaAnuncioForm(forms.ModelForm):
#     class Meta:
#         model = OfertaAnuncio
#         fields = ['anuncio', 'precio_oferta']
#
#     def __init__(self, *args, **kwargs):
#         self.usuario = kwargs.pop('usuario', None)
#         super().__init__(*args, **kwargs)
#
#     def clean_precio_oferta(self):
#         precio_oferta = self.cleaned_data['precio_oferta']
#         anuncio = self.cleaned_data['anuncio']
#
#         # Validar si el precio de la oferta es mayor que el precio inicial del anuncio
#         if precio_oferta <= anuncio.precio_inicial:
#             raise forms.ValidationError("La oferta debe ser mayor al precio inicial del artículo.")
#
#         # Validar si la oferta es mayor a las ofertas anteriores
#         ultima_oferta = anuncio.ofertas.order_by('-precio_oferta').first()
#         if ultima_oferta and precio_oferta <= ultima_oferta.precio_oferta:
#             raise forms.ValidationError("La oferta debe ser mayor que la oferta más alta actual.")
#
#         return precio_oferta