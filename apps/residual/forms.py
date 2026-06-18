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
        prob_res = cleaned.get('prob_residual')
        imp_res = cleaned.get('impacto_residual')
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
    """Formulario exclusivo para auditor: registrar decisión de aceptación."""
    class Meta:
        model = RiesgoResidual
        fields = ['aceptacion', 'resp_aprobacion', 'observaciones']
        widgets = {
            'aceptacion': forms.Select(attrs={'class': 'form-select'}),
            'resp_aprobacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
