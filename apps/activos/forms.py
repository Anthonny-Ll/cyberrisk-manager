from django import forms
from apps.validadores import validar_texto_descriptivo
from .models import Activo


class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = ['nombre', 'tipo', 'descripcion', 'propietario', 'departamento',
                  'confidencialidad', 'integridad', 'disponibilidad',
                  'datos_sensibles', 'estado', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'propietario': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'confidencialidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_confidencialidad'}),
            'integridad': forms.Select(attrs={'class': 'form-select', 'id': 'id_integridad'}),
            'disponibilidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_disponibilidad'}),
            'datos_sensibles': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_datos_sensibles'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre(self):
        return validar_texto_descriptivo(self.cleaned_data.get('nombre'), minimo=5, campo='El nombre del activo')

    def clean(self):
        cleaned_data = super().clean()
        # RN-06: datos sensibles → confidencialidad = 4
        if cleaned_data.get('datos_sensibles'):
            cleaned_data['confidencialidad'] = 4
        return cleaned_data
