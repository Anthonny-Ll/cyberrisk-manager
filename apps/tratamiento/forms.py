from django import forms
from .models import Tratamiento


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['id_riesgo', 'estrategia', 'nombre_control', 'descripcion_ctrl',
                  'tipo_control', 'funcion_control', 'responsable', 'fecha_objetivo',
                  'estado_control', 'justificacion']
        widgets = {
            'id_riesgo': forms.Select(attrs={'class': 'form-select'}),
            'estrategia': forms.Select(attrs={'class': 'form-select', 'id': 'id_estrategia'}),
            'nombre_control': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_ctrl': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_control': forms.Select(attrs={'class': 'form-select'}),
            'funcion_control': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_objetivo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_control': forms.Select(attrs={'class': 'form-select'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_justificacion'}),
        }

    def clean(self):
        cleaned = super().clean()
        # RN-04: Estrategia "Aceptar" requiere justificación
        if cleaned.get('estrategia') == 'Aceptar' and not cleaned.get('justificacion', '').strip():
            raise forms.ValidationError('La justificación es obligatoria cuando la estrategia es "Aceptar".')
        return cleaned
