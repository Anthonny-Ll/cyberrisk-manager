from django import forms
from .models import RiesgoResidual


class RiesgoResidualForm(forms.ModelForm):
    class Meta:
        model = RiesgoResidual
        fields = ['id_riesgo', 'id_tratamiento', 'prob_residual', 'impacto_residual', 'observaciones']
        widgets = {
            'id_riesgo': forms.Select(attrs={'class': 'form-select'}),
            'id_tratamiento': forms.Select(attrs={'class': 'form-select'}),
            'prob_residual': forms.Select(attrs={'class': 'form-select', 'id': 'id_prob_residual'}),
            'impacto_residual': forms.Select(attrs={'class': 'form-select', 'id': 'id_impacto_residual'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        riesgo = cleaned.get('id_riesgo')
        tratamiento = cleaned.get('id_tratamiento')
        prob_res = cleaned.get('prob_residual')
        imp_res = cleaned.get('impacto_residual')

        # El tratamiento seleccionado debe pertenecer al riesgo seleccionado
        if riesgo and tratamiento and tratamiento.id_riesgo_id != riesgo.id:
            raise forms.ValidationError(
                f'El tratamiento "{tratamiento.nombre_control}" pertenece al riesgo '
                f'R-{tratamiento.id_riesgo.pk:03d}, no al riesgo seleccionado R-{riesgo.pk:03d}.'
            )

        if riesgo and prob_res and imp_res:
            residual = prob_res * imp_res
            # RN-03: Riesgo residual no puede ser mayor al inherente
            if residual > riesgo.riesgo_inherente:
                raise forms.ValidationError(
                    f'El riesgo residual ({residual}) no puede ser mayor al riesgo inherente ({riesgo.riesgo_inherente}). '
                    'Ajuste los valores de probabilidad e impacto residual.'
                )
        return cleaned


class AceptacionResidualForm(forms.ModelForm):
    """Formulario para registrar la decisión de aceptación del riesgo residual."""
    class Meta:
        model = RiesgoResidual
        fields = ['aceptacion', 'resp_aprobacion', 'observaciones']
        widgets = {
            'aceptacion': forms.Select(attrs={'class': 'form-select'}),
            'resp_aprobacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('aceptacion') in ('Aceptado', 'Rechazado') and not (cleaned.get('resp_aprobacion') or '').strip():
            raise forms.ValidationError(
                'Debe indicar el responsable que aprueba o rechaza la decisión.'
            )
        return cleaned
