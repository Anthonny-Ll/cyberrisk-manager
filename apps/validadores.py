"""Validadores de texto reutilizables para los formularios del sistema."""
import re
from django import forms

_PATRON_LETRAS = re.compile(r'[a-zA-ZÀ-ÿ]{3,}')


def validar_texto_descriptivo(valor, minimo=5, campo='Este campo'):
    """Rechaza texto vacio, demasiado corto, sin letras reales, o de caracter repetido."""
    valor = (valor or '').strip()
    if len(valor) < minimo:
        raise forms.ValidationError(f'{campo} debe tener al menos {minimo} caracteres descriptivos.')
    if not _PATRON_LETRAS.search(valor):
        raise forms.ValidationError(f'{campo} debe contener texto descriptivo, no solo numeros o simbolos.')
    solo_letras = re.sub(r'[^a-zA-ZÀ-ÿ]', '', valor).lower()
    if solo_letras and len(set(solo_letras)) == 1:
        raise forms.ValidationError(f'{campo} no parece un valor valido (caracter repetido).')
    return valor
