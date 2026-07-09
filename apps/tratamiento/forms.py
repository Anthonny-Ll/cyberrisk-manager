from django import forms
from django.utils import timezone
from apps.validadores import validar_texto_descriptivo
from .models import Tratamiento


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['id_riesgo', 'estrategia', 'nombre_control', 'descripcion_ctrl',
                  'tipo_control', 'funcion_control', 'control_iso', 'responsable',
                  'fecha_planificacion', 'fecha_inicio_ejecucion', 'fecha_objetivo', 'fecha_finalizacion',
                  'estado_control', 'justificacion']
        widgets = {
            'id_riesgo': forms.Select(attrs={'class': 'form-select'}),
            'estrategia': forms.Select(attrs={'class': 'form-select', 'id': 'id_estrategia'}),
            'nombre_control': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_ctrl': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_control': forms.Select(attrs={'class': 'form-select'}),
            'funcion_control': forms.Select(attrs={'class': 'form-select'}),
            'control_iso': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_planificacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_inicio_ejecucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_objetivo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_finalizacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_control': forms.Select(attrs={'class': 'form-select'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_justificacion'}),
        }

    def clean_nombre_control(self):
        return validar_texto_descriptivo(self.cleaned_data.get('nombre_control'), minimo=5, campo='El nombre del control')

    def clean_descripcion_ctrl(self):
        return validar_texto_descriptivo(self.cleaned_data.get('descripcion_ctrl'), minimo=15, campo='La descripción del control')

    def clean(self):
        cleaned = super().clean()
        # RN-04: Estrategia "Aceptar" requiere justificación
        if cleaned.get('estrategia') == 'Aceptar' and not cleaned.get('justificacion', '').strip():
            raise forms.ValidationError('La justificación es obligatoria cuando la estrategia es "Aceptar".')

        planificacion = cleaned.get('fecha_planificacion')
        inicio = cleaned.get('fecha_inicio_ejecucion')
        objetivo = cleaned.get('fecha_objetivo')
        finalizacion = cleaned.get('fecha_finalizacion')

        # Un tratamiento nuevo no puede planificarse con fecha objetivo ya vencida
        if objetivo and self.instance.pk is None and objetivo < timezone.now().date():
            raise forms.ValidationError('La fecha objetivo de un nuevo tratamiento no puede estar en el pasado.')

        # Orden logico del ciclo de vida: planificacion <= inicio <= objetivo, y finalizacion no antes del inicio
        if planificacion and objetivo and planificacion > objetivo:
            raise forms.ValidationError('La fecha de planificación no puede ser posterior a la fecha objetivo.')
        if inicio and objetivo and inicio > objetivo:
            raise forms.ValidationError('La fecha de inicio de ejecución no puede ser posterior a la fecha objetivo.')
        if planificacion and inicio and planificacion > inicio:
            raise forms.ValidationError('La fecha de planificación no puede ser posterior a la fecha de inicio de ejecución.')
        if finalizacion and inicio and finalizacion < inicio:
            raise forms.ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio de ejecución.')
        return cleaned
