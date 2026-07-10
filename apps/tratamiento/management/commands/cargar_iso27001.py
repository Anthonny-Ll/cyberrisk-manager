# -*- coding: utf-8 -*-
"""
Carga el catalogo de 93 controles de referencia ISO/IEC 27001:2022 (Anexo A).
Uso: python manage.py cargar_iso27001
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Carga el catalogo de controles ISO/IEC 27001:2022 - Anexo A (93 controles)'

    def handle(self, *args, **options):
        from apps.tratamiento.models import ControlISO27001

        controles = []

        # Clausula 5 - Controles organizacionales (37)
        organizacionales = [
            ('5.1', 'Politicas de seguridad de la informacion'),
            ('5.2', 'Roles y responsabilidades de seguridad de la informacion'),
            ('5.3', 'Segregacion de funciones'),
            ('5.4', 'Responsabilidades de la direccion'),
            ('5.5', 'Contacto con las autoridades'),
            ('5.6', 'Contacto con grupos de interes especial'),
            ('5.7', 'Inteligencia de amenazas'),
            ('5.8', 'Seguridad de la informacion en la gestion de proyectos'),
            ('5.9', 'Inventario de informacion y otros activos asociados'),
            ('5.10', 'Uso aceptable de la informacion y otros activos asociados'),
            ('5.11', 'Devolucion de activos'),
            ('5.12', 'Clasificacion de la informacion'),
            ('5.13', 'Etiquetado de la informacion'),
            ('5.14', 'Transferencia de informacion'),
            ('5.15', 'Control de acceso'),
            ('5.16', 'Gestion de identidad'),
            ('5.17', 'Informacion de autenticacion'),
            ('5.18', 'Derechos de acceso'),
            ('5.19', 'Seguridad de la informacion en las relaciones con proveedores'),
            ('5.20', 'Tratamiento de la seguridad de la informacion en acuerdos con proveedores'),
            ('5.21', 'Gestion de la seguridad de la informacion en la cadena de suministro TIC'),
            ('5.22', 'Seguimiento, revision y gestion de cambios de servicios de proveedores'),
            ('5.23', 'Seguridad de la informacion para el uso de servicios en la nube'),
            ('5.24', 'Planificacion y preparacion de la gestion de incidentes de seguridad'),
            ('5.25', 'Evaluacion y decision sobre eventos de seguridad de la informacion'),
            ('5.26', 'Respuesta a incidentes de seguridad de la informacion'),
            ('5.27', 'Aprendizaje de los incidentes de seguridad de la informacion'),
            ('5.28', 'Recopilacion de evidencias'),
            ('5.29', 'Seguridad de la informacion durante la disrupcion'),
            ('5.30', 'Preparacion TIC para la continuidad del negocio'),
            ('5.31', 'Requisitos legales, estatutarios, reglamentarios y contractuales'),
            ('5.32', 'Derechos de propiedad intelectual'),
            ('5.33', 'Proteccion de registros'),
            ('5.34', 'Privacidad y proteccion de datos personales (PII)'),
            ('5.35', 'Revision independiente de la seguridad de la informacion'),
            ('5.36', 'Cumplimiento de politicas, normas y estandares de seguridad'),
            ('5.37', 'Procedimientos operativos documentados'),
        ]
        for codigo, nombre in organizacionales:
            controles.append((codigo, nombre, 'Organizacional'))

        # Clausula 6 - Controles de personas (8)
        personas = [
            ('6.1', 'Seleccion de personal'),
            ('6.2', 'Terminos y condiciones de empleo'),
            ('6.3', 'Concienciacion, educacion y capacitacion en seguridad de la informacion'),
            ('6.4', 'Proceso disciplinario'),
            ('6.5', 'Responsabilidades tras la finalizacion o cambio de empleo'),
            ('6.6', 'Acuerdos de confidencialidad o no divulgacion'),
            ('6.7', 'Trabajo remoto'),
            ('6.8', 'Reporte de eventos de seguridad de la informacion'),
        ]
        for codigo, nombre in personas:
            controles.append((codigo, nombre, 'Personas'))

        # Clausula 7 - Controles fisicos (14)
        fisicos = [
            ('7.1', 'Perimetros de seguridad fisica'),
            ('7.2', 'Controles de entrada fisica'),
            ('7.3', 'Seguridad de oficinas, despachos y recursos'),
            ('7.4', 'Monitoreo de seguridad fisica'),
            ('7.5', 'Proteccion contra amenazas fisicas y ambientales'),
            ('7.6', 'Trabajo en areas seguras'),
            ('7.7', 'Escritorio y pantalla limpios'),
            ('7.8', 'Emplazamiento y proteccion de equipos'),
            ('7.9', 'Seguridad de los activos fuera de las instalaciones'),
            ('7.10', 'Medios de almacenamiento'),
            ('7.11', 'Servicios de suministro'),
            ('7.12', 'Seguridad del cableado'),
            ('7.13', 'Mantenimiento de equipos'),
            ('7.14', 'Eliminacion segura o reutilizacion de equipos'),
        ]
        for codigo, nombre in fisicos:
            controles.append((codigo, nombre, 'Físico'))

        # Clausula 8 - Controles tecnologicos (34)
        tecnologicos = [
            ('8.1', 'Dispositivos de punto final de usuario'),
            ('8.2', 'Derechos de acceso privilegiado'),
            ('8.3', 'Restriccion de acceso a la informacion'),
            ('8.4', 'Acceso al codigo fuente'),
            ('8.5', 'Autenticacion segura'),
            ('8.6', 'Gestion de capacidad'),
            ('8.7', 'Proteccion contra malware'),
            ('8.8', 'Gestion de vulnerabilidades tecnicas'),
            ('8.9', 'Gestion de configuracion'),
            ('8.10', 'Eliminacion de informacion'),
            ('8.11', 'Enmascaramiento de datos'),
            ('8.12', 'Prevencion de fuga de datos'),
            ('8.13', 'Copias de seguridad de la informacion'),
            ('8.14', 'Redundancia de instalaciones de procesamiento'),
            ('8.15', 'Registro de eventos (logging)'),
            ('8.16', 'Actividades de monitoreo'),
            ('8.17', 'Sincronizacion de relojes'),
            ('8.18', 'Uso de programas utilitarios privilegiados'),
            ('8.19', 'Instalacion de software en sistemas operativos'),
            ('8.20', 'Seguridad de redes'),
            ('8.21', 'Seguridad de los servicios de red'),
            ('8.22', 'Segregacion de redes'),
            ('8.23', 'Filtrado web'),
            ('8.24', 'Uso de criptografia'),
            ('8.25', 'Ciclo de vida de desarrollo seguro'),
            ('8.26', 'Requisitos de seguridad de las aplicaciones'),
            ('8.27', 'Principios de arquitectura y ingenieria de sistemas seguros'),
            ('8.28', 'Codificacion segura'),
            ('8.29', 'Pruebas de seguridad en desarrollo y aceptacion'),
            ('8.30', 'Desarrollo externalizado'),
            ('8.31', 'Separacion de entornos de desarrollo, prueba y produccion'),
            ('8.32', 'Gestion de cambios'),
            ('8.33', 'Informacion de prueba'),
            ('8.34', 'Proteccion de sistemas de informacion durante pruebas de auditoria'),
        ]
        for codigo, nombre in tecnologicos:
            controles.append((codigo, nombre, 'Tecnológico'))

        creados = 0
        for codigo, nombre, categoria in controles:
            _, creado = ControlISO27001.objects.get_or_create(
                codigo=codigo, defaults={'nombre': nombre, 'categoria': categoria}
            )
            if creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(
            f'Catalogo ISO 27001:2022 (Anexo A) cargado: {creados} controles nuevos ({len(controles)} totales en catalogo).'
        ))
