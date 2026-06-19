# -*- coding: utf-8 -*-
"""
Comando para crear datos de prueba del sistema CyberSave.
Uso: python manage.py crear_datos
"""
from django.core.management.base import BaseCommand
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Crea datos de prueba para demostracion del sistema'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de prueba...')
        self._crear_usuarios()
        self._crear_activos()
        self._crear_amenazas()
        self._crear_vulnerabilidades()
        self._crear_riesgos()
        self._crear_tratamientos()
        self._crear_residuales()
        self.stdout.write(self.style.SUCCESS('\nDatos de prueba creados correctamente.'))
        self.stdout.write('Credenciales:')
        self.stdout.write('  admin / Admin1234    (Administrador)')
        self.stdout.write('  analista / Analista1234 (Analista)')
        self.stdout.write('  auditor / Auditor1234  (Auditor)')

    def _crear_usuarios(self):
        from apps.usuarios.models import Usuario
        datos_usuarios = [
            {'username': 'admin', 'email': 'admin@cyberrisk.com', 'password': 'Admin1234',
             'nombre_completo': 'Administrador del Sistema', 'rol': 'administrador',
             'is_staff': True, 'is_superuser': True},
            {'username': 'analista', 'email': 'analista@cyberrisk.com', 'password': 'Analista1234',
             'nombre_completo': 'Maria Gonzalez - CISO', 'rol': 'analista'},
            {'username': 'auditor', 'email': 'auditor@cyberrisk.com', 'password': 'Auditor1234',
             'nombre_completo': 'Carlos Mendoza - Director', 'rol': 'auditor'},
            {'username': 'responsable', 'email': 'responsable@cyberrisk.com', 'password': 'Responsable1234',
             'nombre_completo': 'Ana Torres - Jefe TI', 'rol': 'responsable'},
        ]
        self._usuarios = {}
        for datos in datos_usuarios:
            pwd = datos.pop('password')
            u, creado = Usuario.objects.get_or_create(username=datos['username'], defaults=datos)
            if creado:
                u.set_password(pwd)
                u.save()
                self.stdout.write(f'  [OK] Usuario: {u.username}')
            self._usuarios[u.username] = u

    def _crear_activos(self):
        from apps.activos.models import Activo
        datos_activos = [
            {'nombre': 'Base de Datos de Clientes', 'tipo': 'Datos',
             'descripcion': 'Base de datos con informacion personal de clientes (nombres, correos, RUC).',
             'propietario': self._usuarios['responsable'], 'departamento': 'Tecnologia',
             'confidencialidad': 4, 'integridad': 4, 'disponibilidad': 3,
             'datos_sensibles': True, 'observaciones': 'Sujeta a normativa LOPDP'},
            {'nombre': 'Sistema ERP Financiero', 'tipo': 'Software',
             'descripcion': 'Sistema integrado de gestion empresarial para contabilidad y finanzas.',
             'propietario': self._usuarios['responsable'], 'departamento': 'Finanzas',
             'confidencialidad': 4, 'integridad': 4, 'disponibilidad': 4,
             'datos_sensibles': False, 'observaciones': ''},
            {'nombre': 'Servidor Web Corporativo', 'tipo': 'Hardware',
             'descripcion': 'Servidor Dell PowerEdge que aloja el sitio web y servicios externos.',
             'propietario': self._usuarios['responsable'], 'departamento': 'Tecnologia',
             'confidencialidad': 2, 'integridad': 3, 'disponibilidad': 4,
             'datos_sensibles': False, 'observaciones': ''},
            {'nombre': 'Red LAN Corporativa', 'tipo': 'Red',
             'descripcion': 'Infraestructura de red interna: switches, routers y WiFi.',
             'propietario': self._usuarios['responsable'], 'departamento': 'Tecnologia',
             'confidencialidad': 3, 'integridad': 3, 'disponibilidad': 4,
             'datos_sensibles': False, 'observaciones': ''},
            {'nombre': 'Correo Corporativo (Microsoft 365)', 'tipo': 'Servicio',
             'descripcion': 'Servicio de correo electronico corporativo en la nube.',
             'propietario': self._usuarios['responsable'], 'departamento': 'Administracion',
             'confidencialidad': 3, 'integridad': 2, 'disponibilidad': 3,
             'datos_sensibles': False, 'observaciones': ''},
        ]
        self._activos = []
        for datos in datos_activos:
            activo, creado = Activo.objects.get_or_create(nombre=datos['nombre'], defaults=datos)
            if creado:
                self.stdout.write(f'  [OK] Activo: {activo.nombre}')
            self._activos.append(activo)

    def _crear_amenazas(self):
        from apps.amenazas.models import Amenaza, ActivoAmenaza
        datos_amenazas = [
            {'nombre': 'Ataque de Ransomware', 'tipo_amenaza': 'Humana deliberada', 'fuente_amenaza': 'Externa',
             'descripcion': 'Malware que cifra archivos y exige rescate economico.', 'activos_idx': [0, 1, 2]},
            {'nombre': 'Ingenieria Social / Phishing', 'tipo_amenaza': 'Humana deliberada', 'fuente_amenaza': 'Externa',
             'descripcion': 'Engano a empleados para obtener credenciales via correos falsos.', 'activos_idx': [4, 0]},
            {'nombre': 'Acceso no autorizado interno', 'tipo_amenaza': 'Humana deliberada', 'fuente_amenaza': 'Interna',
             'descripcion': 'Empleado con privilegios excesivos accede a informacion confidencial.', 'activos_idx': [0, 1]},
            {'nombre': 'Fallo de energia electrica', 'tipo_amenaza': 'Natural', 'fuente_amenaza': 'Externa',
             'descripcion': 'Corte electrico que afecta la disponibilidad de sistemas.', 'activos_idx': [2, 3]},
            {'nombre': 'Vulnerabilidad en software desactualizado', 'tipo_amenaza': 'Tecnologica', 'fuente_amenaza': 'Mixta',
             'descripcion': 'Explotacion de fallos de seguridad en sistemas sin parches.', 'activos_idx': [1, 2]},
        ]
        self._amenazas = []
        for datos in datos_amenazas:
            idx_list = datos.pop('activos_idx')
            amenaza, creado = Amenaza.objects.get_or_create(nombre=datos['nombre'], defaults=datos)
            for idx in idx_list:
                ActivoAmenaza.objects.get_or_create(id_activo=self._activos[idx], id_amenaza=amenaza)
            if creado:
                self.stdout.write(f'  [OK] Amenaza: {amenaza.nombre}')
            self._amenazas.append(amenaza)

    def _crear_vulnerabilidades(self):
        from apps.vulnerabilidades.models import Vulnerabilidad
        datos_vulns = [
            {'nombre': 'Contrasenas debiles en cuentas de administrador', 'id_activo': self._activos[0],
             'cvss_score': 8.1, 'severidad': 'Alta', 'estado': 'Identificada',
             'descripcion': 'Las cuentas de admin usan contrasenas simples sin politica de complejidad.',
             'evidencia': 'Auditoria interna detectó 3 cuentas con contrasenas triviales.'},
            {'nombre': 'Sin autenticacion multifactor (MFA)', 'id_activo': self._activos[1],
             'cvss_score': 7.5, 'severidad': 'Alta', 'estado': 'En tratamiento',
             'descripcion': 'El ERP no requiere segundo factor para acceso remoto.',
             'evidencia': 'Revision de configuracion de acceso remoto.'},
            {'nombre': 'Parches de seguridad pendientes (CVE-2024-1234)', 'id_activo': self._activos[2],
             'cvss_score': 9.8, 'severidad': 'Crítica', 'estado': 'Identificada',
             'descripcion': 'Servidor con Apache 2.4.51 vulnerable a ejecucion remota de codigo.',
             'evidencia': 'Escaneo con Nessus. CVE-2024-1234 sin parche aplicado.'},
            {'nombre': 'Falta de segmentacion de red', 'id_activo': self._activos[3],
             'cvss_score': 5.5, 'severidad': 'Media', 'estado': 'Identificada',
             'descripcion': 'Red LAN sin VLANs; todos los equipos comparten el mismo segmento.',
             'evidencia': 'Diagrama de red sin segmentacion.'},
            {'nombre': 'Cifrado debil en transmision de correos', 'id_activo': self._activos[4],
             'cvss_score': 3.7, 'severidad': 'Baja', 'estado': 'Resuelta',
             'descripcion': 'Clientes de correo configurados con TLS 1.0 (deprecado).',
             'evidencia': 'Resuelto con actualizacion de politica TLS.'},
        ]
        self._vulns = []
        for datos in datos_vulns:
            vuln, creado = Vulnerabilidad.objects.get_or_create(nombre=datos['nombre'], defaults=datos)
            if creado:
                self.stdout.write(f'  [OK] Vulnerabilidad: {vuln.nombre}')
            self._vulns.append(vuln)

    def _crear_riesgos(self):
        from apps.riesgos.models import Riesgo
        usuario = self._usuarios['analista']
        datos_riesgos = [
            {'id_activo': self._activos[0], 'id_amenaza': self._amenazas[0], 'id_vulnerabilidad': self._vulns[0],
             'probabilidad': 3, 'impacto': 4, 'estado_riesgo': 'En tratamiento',
             'id_usuario_registra': usuario, 'observaciones': 'Riesgo prioritario. Contrasenas debiles + ransomware.'},
            {'id_activo': self._activos[2], 'id_amenaza': self._amenazas[4], 'id_vulnerabilidad': self._vulns[2],
             'probabilidad': 4, 'impacto': 4, 'estado_riesgo': 'Evaluado',
             'id_usuario_registra': usuario, 'observaciones': 'CVE-2024-1234 CVSS 9.8. Servidor expuesto a internet.'},
            {'id_activo': self._activos[1], 'id_amenaza': self._amenazas[1], 'id_vulnerabilidad': self._vulns[1],
             'probabilidad': 3, 'impacto': 3, 'estado_riesgo': 'En tratamiento',
             'id_usuario_registra': usuario, 'observaciones': 'Phishing es el vector de ataque mas frecuente.'},
            {'id_activo': self._activos[0], 'id_amenaza': self._amenazas[2], 'id_vulnerabilidad': self._vulns[0],
             'probabilidad': 2, 'impacto': 3, 'estado_riesgo': 'Con residual',
             'id_usuario_registra': usuario, 'observaciones': 'Control de privilegios insuficiente. RBAC en implementacion.'},
            {'id_activo': self._activos[3], 'id_amenaza': self._amenazas[3], 'id_vulnerabilidad': self._vulns[3],
             'probabilidad': 2, 'impacto': 2, 'estado_riesgo': 'Evaluado',
             'id_usuario_registra': usuario, 'observaciones': 'Sin UPS en cuarto de comunicaciones.'},
        ]
        self._riesgos = []
        for datos in datos_riesgos:
            riesgo, creado = Riesgo.objects.get_or_create(
                id_activo=datos['id_activo'], id_amenaza=datos['id_amenaza'],
                id_vulnerabilidad=datos['id_vulnerabilidad'], defaults=datos
            )
            if creado:
                self.stdout.write(f'  [OK] Riesgo R-{riesgo.pk:03d}: {riesgo.nivel_cualitativo} ({riesgo.riesgo_inherente})')
            self._riesgos.append(riesgo)

    def _crear_tratamientos(self):
        from apps.tratamiento.models import Tratamiento
        hoy = date.today()
        datos_tratamientos = [
            {'id_riesgo': self._riesgos[0], 'estrategia': 'Mitigar',
             'nombre_control': 'Implementar politica de contrasenas fuertes',
             'descripcion_ctrl': 'Configurar minimo 12 caracteres con complejidad. Bloquear tras 5 intentos fallidos.',
             'tipo_control': 'Técnico', 'funcion_control': 'Preventivo',
             'responsable': 'Jefe de Infraestructura TI', 'fecha_objetivo': hoy + timedelta(days=15),
             'estado_control': 'En progreso'},
            {'id_riesgo': self._riesgos[2], 'estrategia': 'Mitigar',
             'nombre_control': 'Activar autenticacion multifactor (MFA)',
             'descripcion_ctrl': 'Implementar MFA con Google/Microsoft Authenticator para todos los accesos al ERP.',
             'tipo_control': 'Técnico', 'funcion_control': 'Preventivo',
             'responsable': 'Administrador de Sistemas', 'fecha_objetivo': hoy + timedelta(days=30),
             'estado_control': 'Pendiente'},
            {'id_riesgo': self._riesgos[3], 'estrategia': 'Mitigar',
             'nombre_control': 'Implementar control de acceso basado en roles (RBAC)',
             'descripcion_ctrl': 'Revisar y redefinir permisos aplicando principio de minimo privilegio.',
             'tipo_control': 'Administrativo', 'funcion_control': 'Preventivo',
             'responsable': 'DBA y Administrador de Seguridad', 'fecha_objetivo': hoy - timedelta(days=5),
             'estado_control': 'Pendiente'},
        ]
        self._tratamientos = []
        for datos in datos_tratamientos:
            trat, creado = Tratamiento.objects.get_or_create(
                id_riesgo=datos['id_riesgo'], nombre_control=datos['nombre_control'], defaults=datos
            )
            if creado:
                self.stdout.write(f'  [OK] Tratamiento: {trat.nombre_control[:50]}')
            self._tratamientos.append(trat)

    def _crear_residuales(self):
        from apps.residual.models import RiesgoResidual
        from django.utils import timezone
        datos_residuales = [
            {'id_riesgo': self._riesgos[3], 'id_tratamiento': self._tratamientos[2],
             'prob_residual': 1, 'impacto_residual': 2, 'aceptacion': 'Aceptado',
             'resp_aprobacion': 'Carlos Mendoza - Director',
             'id_usuario_aprueba': self._usuarios['auditor'],
             'fecha_decision': timezone.now(),
             'observaciones': 'Riesgo residual aceptable tras implementacion de RBAC.'},
            {'id_riesgo': self._riesgos[0], 'id_tratamiento': self._tratamientos[0],
             'prob_residual': 2, 'impacto_residual': 3, 'aceptacion': 'Pendiente',
             'resp_aprobacion': '', 'observaciones': 'En espera de revision por la alta direccion.'},
        ]
        for datos in datos_residuales:
            residual, creado = RiesgoResidual.objects.get_or_create(
                id_riesgo=datos['id_riesgo'], defaults=datos
            )
            if creado:
                self.stdout.write(f'  [OK] Residual RR-{residual.pk:03d}: {residual.nivel_cualitativo} ({residual.riesgo_residual})')
