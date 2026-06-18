from django import forms
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
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'confidencialidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_confidencialidad'}),
            'integridad': forms.Select(attrs={'class': 'form-select', 'id': 'id_integridad'}),
            'disponibilidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_disponibilidad'}),
            'datos_sensibles': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_datos_sensibles'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # RN-06: datos sensibles → confidencialidad = 4
        if cleaned_data.get('datos_sensibles'):
            cleaned_data['confidencialidad'] = 4
        return cleaned_data
