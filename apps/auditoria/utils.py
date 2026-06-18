"""Función utilitaria para registrar eventos en el log de auditoría."""
from .models import LogAuditoria


def registrar_log(usuario, accion, entidad, id_entidad, descripcion):
    """Crea un registro en LogAuditoria. Silencia errores para no interrumpir flujo."""
    try:
        LogAuditoria.objects.create(
            id_usuario=usuario,
            accion=accion,
            entidad_afectada=entidad,
            id_entidad=id_entidad,
            descripcion=descripcion,
        )
    except Exception:
        pass
