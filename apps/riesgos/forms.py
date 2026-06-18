from django import forms
from apps.activos.models import Activo
from .models import Riesgo


class RiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = ['id_activo', 'id_amenaza', 'id_vulnerabilidad', 'probabilidad', 'impacto',
                  'estado_riesgo', 'observaciones']
        widgets = {
            'id_activo': forms.Select(attrs={'class': 'form-select'}),
            'id_amenaza': forms.Select(attrs={'class': 'form-select'}),
            'id_vulnerabilidad': forms.Select(attrs={'class': 'form-select'}),
            'probabilidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_probabilidad'}),
            'impacto': forms.Select(attrs={'class': 'form-select', 'id': 'id_impacto'}),
            'estado_riesgo': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        # RN-02: activo + amenaza + vulnerabilidad obligatorios
        if not cleaned.get('id_activo') or not cleaned.get('id_amenaza') or not cleaned.get('id_vulnerabilidad'):
            raise forms.ValidationError('Debe seleccionar activo, amenaza y vulnerabilidad.')
        # RN-10: Activo desactivado no puede asociarse
        activo = cleaned.get('id_activo')
        if activo and activo.estado == 'Inactivo':
            raise forms.ValidationError('El activo seleccionado está inactivo y no puede usarse.')
        return cleaned
