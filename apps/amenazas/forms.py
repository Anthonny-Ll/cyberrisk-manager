from django import forms
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
