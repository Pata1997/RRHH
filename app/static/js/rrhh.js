// Inicializar DataTables
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar DataTables si existe tabla con clase 'datatable'
    if (document.querySelectorAll('.datatable').length > 0) {
        initDataTables();
    }
    
    // Inicializar tooltips de Bootstrap
    initTooltips();
});

function initDataTables() {
    const tables = document.querySelectorAll('.datatable');
    tables.forEach(table => {
        if (!$.fn.DataTable.isDataTable(table)) {
            $(table).DataTable({
                language: {
                    lengthMenu: 'Mostrar _MENU_ registros',
                    zeroRecords: 'No se encontraron registros',
                    info: 'Mostrando de _START_ a _END_ de _TOTAL_ registros',
                    infoEmpty: 'Mostrando 0 registros',
                    infoFiltered: '(filtrado de _MAX_ registros totales)',
                    search: 'Buscar:',
                    paginate: {
                        first: 'Primero',
                        last: 'Último',
                        next: 'Siguiente',
                        previous: 'Anterior'
                    }
                },
                pageLength: 10,
                responsive: true,
                dom: 'lBfrtip',
                buttons: [
                    {
                        extend: 'excel',
                        text: '<i class="bi bi-file-earmark-spreadsheet"></i> Excel',
                        className: 'btn btn-sm btn-success'
                    },
                    {
                        extend: 'pdf',
                        text: '<i class="bi bi-file-earmark-pdf"></i> PDF',
                        className: 'btn btn-sm btn-danger'
                    },
                    {
                        extend: 'print',
                        text: '<i class="bi bi-printer"></i> Imprimir',
                        className: 'btn btn-sm btn-info'
                    }
                ]
            });
        }
    });
}

function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Función para mostrar confirmación con SweetAlert2
function confirmar(titulo, mensaje, callback) {
    Swal.fire({
        title: titulo,
        text: mensaje,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#003366',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Confirmar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            if (callback) callback();
        }
    });
}

// Función para mostrar mensaje exitoso
function mostrarExito(titulo, mensaje = '') {
    Swal.fire({
        icon: 'success',
        title: titulo,
        text: mensaje,
        timer: 3000,
        timerProgressBar: true
    });
}

// Función para mostrar mensaje de error
function mostrarError(titulo, mensaje = '') {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje
    });
}

// Función para mostrar información
function mostrarInfo(titulo, mensaje = '') {
    Swal.fire({
        icon: 'info',
        title: titulo,
        text: mensaje
    });
}

// Formatear moneda
function formatoMoneda(valor) {
    return new Intl.NumberFormat('es-PY', {
        style: 'currency',
        currency: 'PYG',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(valor);
}

// Formatear fecha
function formatoFecha(fecha) {
    return new Intl.DateTimeFormat('es-PY', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    }).format(new Date(fecha));
}

// Copiar al portapapeles
function copiarAlPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        mostrarExito('Copiado', 'El texto ha sido copiado al portapapeles');
    }).catch(() => {
        mostrarError('Error', 'No se pudo copiar al portapapeles');
    });
}

// Validación de formularios
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Limpiar formulario
function limpiarFormulario(formId) {
    const form = document.getElementById(formId);
    form.reset();
    form.classList.remove('was-validated');
}

// Hacer visible la contraseña
function alternarMostrarPassword(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

// Cargar más registros (pagination manual)
function cargarMas(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.querySelector('table tbody').insertAdjacentHTML('beforeend', html);
            if (document.querySelectorAll('.datatable').length > 0) {
                initDataTables();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarError('Error', 'No se pudieron cargar más registros');
        });
}

// Auto-cerrar alertas después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alertas = document.querySelectorAll('.alert');
    alertas.forEach(alerta => {
        setTimeout(() => {
            alerta.style.opacity = '0';
            setTimeout(() => alerta.remove(), 300);
        }, 5000);
    });
});

// Prevenir envío doble de formularios
document.addEventListener('DOMContentLoaded', function() {
    const formularios = document.querySelectorAll('form');
    formularios.forEach(formulario => {
        formulario.addEventListener('submit', function() {
            const botones = this.querySelectorAll('button[type="submit"]');
            botones.forEach(boton => {
                boton.disabled = true;
                boton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
            });
        });
    });
});

// Filtro en tiempo real
function filtroTiempoReal(inputId, tableName) {
    const input = document.getElementById(inputId);
    const tabla = document.querySelector(tableName);
    const filas = tabla.querySelectorAll('tbody tr');
    
    input.addEventListener('keyup', function() {
        const filtro = this.value.toUpperCase();
        filas.forEach(fila => {
            const texto = fila.textContent.toUpperCase();
            fila.style.display = texto.includes(filtro) ? '' : 'none';
        });
    });
}
