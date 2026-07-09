from django import forms
from apps.validadores import validar_texto_descriptivo
from .models import Vulnerabilidad


class VulnerabilidadForm(forms.ModelForm):
    class Meta:
        model = Vulnerabilidad
        fields = ['nombre', 'cve_id', 'descripcion', 'id_activo', 'amenaza_asociada',
                  'cvss_score', 'cvss_vector', 'severidad', 'evidencia', 'estado', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cve_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVE-YYYY-NNNN', 'id': 'id_cve_id'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'id_activo': forms.Select(attrs={'class': 'form-select'}),
            'amenaza_asociada': forms.Select(attrs={'class': 'form-select'}),
            'cvss_score': forms.NumberInput(attrs={
                'class': 'form-control fw-bold', 'step': '0.1', 'min': '0', 'max': '10',
                'id': 'id_cvss_score', 'readonly': 'readonly'}),
            'cvss_vector': forms.TextInput(attrs={
                'class': 'form-control font-monospace small', 'id': 'id_cvss_vector', 'readonly': 'readonly'}),
            'severidad': forms.Select(attrs={'class': 'form-select', 'id': 'id_severidad'}),
            'evidencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_nombre(self):
        return validar_texto_descriptivo(self.cleaned_data.get('nombre'), minimo=5, campo='El nombre de la vulnerabilidad')

    def clean(self):
        cleaned = super().clean()
        # El puntaje puede venir de la calculadora CVSS (cvss_vector) o de una busqueda
        # de CVE real en el NIST (cve_id); cualquiera de los dos caminos es valido.
        cvss_vector = cleaned.get('cvss_vector')
        cve_id = (cleaned.get('cve_id') or '').strip()
        cvss_score = cleaned.get('cvss_score')
        if cvss_score is None or not (cvss_vector or cve_id):
            raise forms.ValidationError(
                'Debe usar la calculadora CVSS o buscar un CVE real en el NIST para obtener un puntaje válido antes de guardar.'
            )
        cleaned['severidad'] = Vulnerabilidad._cvss_a_severidad(cvss_score)
        estado = cleaned.get('estado')
        evidencia = (cleaned.get('evidencia') or '').strip()
        if estado in ('En tratamiento', 'Resuelta') and len(evidencia) < 10:
            raise forms.ValidationError(
                f'Para marcar el estado como "{estado}" debe documentar evidencia (mínimo 10 caracteres).'
            )
        return cleaned
