from django import forms
from .models import Vulnerabilidad


class VulnerabilidadForm(forms.ModelForm):
    class Meta:
        model = Vulnerabilidad
        fields = ['nombre', 'descripcion', 'id_activo', 'cvss_score', 'severidad', 'evidencia', 'estado', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'id_activo': forms.Select(attrs={'class': 'form-select'}),
            'cvss_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '10', 'id': 'id_cvss_score'}),
            'severidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_severidad'}),
            'evidencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
