from django import forms
from apps.validadores import validar_texto_descriptivo
from .models import Amenaza


class AmenazaForm(forms.ModelForm):
    class Meta:
        model = Amenaza
        fields = ['nombre', 'descripcion', 'tipo_amenaza', 'fuente_amenaza', 'activos', 'estado', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_amenaza': forms.Select(attrs={'class': 'form-select'}),
            'fuente_amenaza': forms.Select(attrs={'class': 'form-select'}),
            'activos': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre(self):
        return validar_texto_descriptivo(self.cleaned_data.get('nombre'), minimo=5, campo='El nombre de la amenaza')

    def clean_activos(self):
        activos = self.cleaned_data.get('activos')
        if not activos or activos.count() == 0:
            raise forms.ValidationError('Debe asociar la amenaza a al menos un activo existente.')
        return activos
