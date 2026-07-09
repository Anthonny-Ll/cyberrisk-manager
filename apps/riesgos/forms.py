from django import forms
from apps.activos.models import Activo
from apps.amenazas.models import ActivoAmenaza
from .models import Riesgo


class RiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = ['id_activo', 'id_amenaza', 'id_vulnerabilidad', 'probabilidad', 'impacto',
                  'estado_riesgo', 'controles_existentes', 'observaciones']
        widgets = {
            'id_activo': forms.Select(attrs={'class': 'form-select'}),
            'id_amenaza': forms.Select(attrs={'class': 'form-select'}),
            'id_vulnerabilidad': forms.Select(attrs={'class': 'form-select'}),
            'probabilidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_probabilidad'}),
            'impacto': forms.Select(attrs={'class': 'form-select', 'id': 'id_impacto'}),
            'estado_riesgo': forms.Select(attrs={'class': 'form-select'}),
            'controles_existentes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        # RN-02: activo + amenaza + vulnerabilidad obligatorios
        activo = cleaned.get('id_activo')
        amenaza = cleaned.get('id_amenaza')
        vulnerabilidad = cleaned.get('id_vulnerabilidad')
        if not activo or not amenaza or not vulnerabilidad:
            raise forms.ValidationError('Debe seleccionar activo, amenaza y vulnerabilidad.')
        # RN-10: Activo desactivado no puede asociarse
        if activo.estado == 'Inactivo':
            raise forms.ValidationError('El activo seleccionado está inactivo y no puede usarse.')
        # Validación cruzada: la amenaza debe estar vinculada al activo
        if not ActivoAmenaza.objects.filter(id_activo=activo, id_amenaza=amenaza).exists():
            raise forms.ValidationError(
                f'La amenaza "{amenaza}" no está asociada al activo "{activo}". '
                'Vincúlelas primero en el módulo de Amenazas.'
            )
        # Validación cruzada: la vulnerabilidad debe pertenecer al activo
        if vulnerabilidad.id_activo_id != activo.id:
            raise forms.ValidationError(
                f'La vulnerabilidad "{vulnerabilidad}" pertenece al activo "{vulnerabilidad.id_activo}", '
                f'no al activo seleccionado "{activo}".'
            )
        return cleaned
