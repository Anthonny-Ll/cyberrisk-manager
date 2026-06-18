"""Filtros personalizados para templates de riesgos."""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Permite acceder a diccionarios con claves dinámicas en templates."""
    return dictionary.get(key)
