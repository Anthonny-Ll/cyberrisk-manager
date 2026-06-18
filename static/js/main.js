/* CyberRisk Manager — JavaScript principal */

// Toggle del menú lateral
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Auto-dismiss alertas después de 5 segundos
    const alertas = document.querySelectorAll('.alert.alert-success');
    alertas.forEach(function (alerta) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
            bsAlert.close();
        }, 5000);
    });
});

// Cálculo en tiempo real del riesgo inherente (formulario de riesgos)
function calcularRiesgo() {
    const prob = parseInt(document.getElementById('id_probabilidad')?.value || 0);
    const imp  = parseInt(document.getElementById('id_impacto')?.value || 0);
    const resultado = document.getElementById('resultado-riesgo');
    if (!resultado || !prob || !imp) return;

    const valor = prob * imp;
    let nivel = '', color = '';
    if (valor <= 4)       { nivel = 'BAJO';    color = '#28a745'; }
    else if (valor <= 8)  { nivel = 'MEDIO';   color = '#ffc107'; }
    else if (valor <= 12) { nivel = 'ALTO';    color = '#fd7e14'; }
    else                  { nivel = 'CRÍTICO'; color = '#dc3545'; }

    resultado.innerHTML =
        `<strong>Riesgo inherente: <span style="font-size:1.4rem;color:${color}">${valor}</span></strong>
         <span class="badge ms-2" style="background-color:${color};color:${valor>=5&&valor<=8?'#212529':'#fff'}">${nivel}</span>`;
}

document.addEventListener('DOMContentLoaded', function () {
    ['id_probabilidad', 'id_impacto'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', calcularRiesgo);
    });
    calcularRiesgo();
});

// Cálculo en tiempo real del riesgo residual
function calcularResidual() {
    const prob = parseInt(document.getElementById('id_prob_residual')?.value || 0);
    const imp  = parseInt(document.getElementById('id_impacto_residual')?.value || 0);
    const resultado = document.getElementById('resultado-residual');
    const inherenteEl = document.getElementById('riesgo-inherente-ref');
    if (!resultado || !prob || !imp) return;

    const valor = prob * imp;
    const inherente = inherenteEl ? parseInt(inherenteEl.dataset.valor || 99) : 99;
    let nivel = '', color = '';
    if (valor <= 4)       { nivel = 'BAJO';    color = '#28a745'; }
    else if (valor <= 8)  { nivel = 'MEDIO';   color = '#ffc107'; }
    else if (valor <= 12) { nivel = 'ALTO';    color = '#fd7e14'; }
    else                  { nivel = 'CRÍTICO'; color = '#dc3545'; }

    let warning = '';
    if (valor > inherente) {
        warning = `<div class="alert alert-danger py-1 mt-2 small">⚠️ El riesgo residual (${valor}) supera el inherente (${inherente}). No se puede guardar.</div>`;
    }

    resultado.innerHTML =
        `<strong>Riesgo residual: <span style="font-size:1.4rem;color:${color}">${valor}</span></strong>
         <span class="badge ms-2" style="background-color:${color};color:${valor>=5&&valor<=8?'#212529':'#fff'}">${nivel}</span>
         ${warning}`;
}

document.addEventListener('DOMContentLoaded', function () {
    ['id_prob_residual', 'id_impacto_residual'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', calcularResidual);
    });
    calcularResidual();
});

// Mostrar/ocultar campo justificación según estrategia
document.addEventListener('DOMContentLoaded', function () {
    const estrategia = document.getElementById('id_estrategia');
    const justRow = document.getElementById('justificacion-row');
    if (!estrategia || !justRow) return;

    function toggleJustificacion() {
        justRow.style.display = estrategia.value === 'Aceptar' ? 'block' : 'none';
    }
    estrategia.addEventListener('change', toggleJustificacion);
    toggleJustificacion();
});

// Sugerencia automática de severidad desde CVSS
document.addEventListener('DOMContentLoaded', function () {
    const cvss = document.getElementById('id_cvss_score');
    const severidad = document.getElementById('id_severidad');
    if (!cvss || !severidad) return;

    cvss.addEventListener('input', function () {
        const score = parseFloat(this.value);
        if (isNaN(score)) return;
        if (score < 4.0)       severidad.value = 'Baja';
        else if (score < 7.0)  severidad.value = 'Media';
        else if (score < 9.0)  severidad.value = 'Alta';
        else                   severidad.value = 'Crítica';
    });
});

// Auto-forzar confidencialidad=4 si datos_sensibles está marcado
document.addEventListener('DOMContentLoaded', function () {
    const datosSensibles = document.getElementById('id_datos_sensibles');
    const confidencialidad = document.getElementById('id_confidencialidad');
    if (!datosSensibles || !confidencialidad) return;

    function aplicarReglaSensibles() {
        if (datosSensibles.checked) {
            confidencialidad.value = '4';
            confidencialidad.disabled = true;
        } else {
            confidencialidad.disabled = false;
        }
    }
    datosSensibles.addEventListener('change', aplicarReglaSensibles);
    aplicarReglaSensibles();
});

// Confirmación modal antes de desactivar
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm || '¿Confirma esta acción?')) {
                e.preventDefault();
            }
        });
    });
});
