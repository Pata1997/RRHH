/**
 * empleado_perfil.js
 * Manejo de tabs y carga dinámica de datos para el legajo digital del empleado
 */

// Funciones de utilidad
function mostrarCarga(elemento) {
    elemento.innerHTML = `
        <div class="loading">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        </div>
    `;
}

function mostrarError(elemento, mensaje) {
    elemento.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle"></i> ${mensaje}
        </div>
    `;
}

function formatearMoneda(valor) {
    return new Intl.NumberFormat('es-PY', {
        style: 'currency',
        currency: 'PYG'
    }).format(valor);
}

// ========== TAB GENERAL ==========
function cargarGeneral() {
    const contenedor = document.getElementById('general-content');
    mostrarCarga(contenedor);
    
    fetch(`/rrhh/api/empleados/${empleadoId}/general`)
        .then(response => response.json())
        .then(data => {
            let html = `
                <div class="col-md-3 mb-3">
                    <div class="kpi-card">
                        <div class="numero">${data.asistencia_mes}</div>
                        <div class="label">Asistencia Mes</div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="kpi-card">
                        <div class="numero">${data.vacaciones_pendientes}</div>
                        <div class="label">Vacaciones Pendientes</div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="kpi-card">
                        <div class="numero">${data.sanciones_activas}</div>
                        <div class="label">Sanciones Activas</div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="kpi-card">
                        <div class="numero">${data.permisos_usados}</div>
                        <div class="label">Permisos Usados</div>
                    </div>
                </div>
                <div class="col-12 mt-4">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Información Laboral</h6>
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Email:</strong> ${data.email || '-'}</p>
                                    <p><strong>Teléfono:</strong> ${data.telefono || '-'}</p>
                                    <p><strong>Salario Base:</strong> ${formatearMoneda(data.salario_base)}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Fecha de Ingreso:</strong> ${data.fecha_ingreso}</p>
                                    <p><strong>Antigüedad:</strong> ${data.antiguedad}</p>
                                    <p><strong>Estado:</strong> <span class="badge bg-${data.estado === 'Activo' ? 'success' : 'danger'}">${data.estado}</span></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-12 mt-4">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">Asistencia de hoy</h6>
                            <p><strong>Entrada:</strong> ${data.resumen_hoy.hora_entrada ? data.resumen_hoy.hora_entrada : '-'}</p>
                            <p><strong>Salida:</strong> ${data.resumen_hoy.hora_salida ? data.resumen_hoy.hora_salida : '-'}</p>
                            <p><strong>Observaciones:</strong> ${data.resumen_hoy.observaciones || '-'}</p>
                        </div>
                    </div>
                </div>
            `;
            contenedor.innerHTML = html;
        })
        .catch(err => mostrarError(contenedor, 'Error al cargar datos generales'));
}

// ========== TAB ASISTENCIAS ==========
function inicializarFiltrosAsistencias() {
    // Llenar meses
    const mesSelect = document.getElementById('asistencias-mes');
    const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    meses.forEach((mes, idx) => {
        const option = document.createElement('option');
        option.value = idx + 1;
        option.textContent = mes;
        mesSelect.appendChild(option);
    });
    
    // Llenar años
    const añoSelect = document.getElementById('asistencias-año');
    const añoActual = new Date().getFullYear();
    for (let i = añoActual; i >= 2020; i--) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        añoSelect.appendChild(option);
    }
}

function cargarAsistencias(pagina) {
    const contenedor = document.getElementById('asistencias-content');
    mostrarCarga(contenedor);
    
    const mes = document.getElementById('asistencias-mes').value;
    const año = document.getElementById('asistencias-año').value;
    
    let url = `/rrhh/api/empleados/${empleadoId}/asistencias?page=${pagina}`;
    if (mes) url += `&mes=${mes}`;
    if (año) url += `&year=${año}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.items.length === 0) {
                contenedor.innerHTML = '<div class="alert alert-info">No hay registros de asistencia</div>';
                return;
            }
            
            let html = `
                <div class="tabla-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Entrada</th>
                                <th>Salida</th>
                                <th>Presente</th>
                                <th>Observaciones</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.items.forEach(a => {
                html += `
                    <tr>
                        <td>${a.fecha}</td>
                        <td>${a.entrada}</td>
                        <td>${a.salida}</td>
                        <td><span class="badge bg-${a.presente === 'Sí' ? 'success' : 'danger'}">${a.presente}</span></td>
                        <td>${a.observaciones}</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            
            // Paginación
            if (data.pages > 1) {
                html += '<nav><ul class="pagination justify-content-center">';
                
                if (data.current_page > 1) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarAsistencias(1)">Primera</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarAsistencias(${data.current_page - 1})">Anterior</button></li>`;
                }
                
                html += `<li class="page-item active"><span class="page-link">${data.current_page} / ${data.pages}</span></li>`;
                
                if (data.current_page < data.pages) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarAsistencias(${data.current_page + 1})">Siguiente</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarAsistencias(${data.pages})">Última</button></li>`;
                }
                
                html += '</ul></nav>';
            }
            
            contenedor.innerHTML = html;
        })
        .catch(err => mostrarError(contenedor, 'Error al cargar asistencias'));
}

// ========== TAB VACACIONES ==========
function cargarVacaciones() {
    const contenedor = document.getElementById('vacaciones-content');
    mostrarCarga(contenedor);
    
    fetch(`/rrhh/api/empleados/${empleadoId}/vacaciones`)
        .then(response => response.json())
        .then(data => {
            if (data.items.length === 0) {
                contenedor.innerHTML = '<div class="alert alert-info">No hay registros de vacaciones</div>';
                return;
            }
            
            let html = `
                <div class="tabla-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Año</th>
                                <th>Disponibles</th>
                                <th>Tomados</th>
                                <th>Pendientes</th>
                                <th>Período</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.items.forEach(v => {
                html += `
                    <tr>
                        <td><strong>${v.año}</strong></td>
                        <td>${v.dias_disponibles}</td>
                        <td>${v.dias_tomados}</td>
                        <td>${v.dias_pendientes}</td>
                        <td>${v.fecha_inicio} a ${v.fecha_fin}</td>
                        <td><span class="badge bg-${v.estado === 'Aprobada' ? 'success' : 'warning'}">${v.estado}</span></td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            contenedor.innerHTML = html;
        })
        .catch(err => mostrarError(contenedor, 'Error al cargar vacaciones'));
}

// ========== TAB PERMISOS ==========
function cargarPermisos(pagina) {
    const contenedor = document.getElementById('permisos-content');
    mostrarCarga(contenedor);
    
    fetch(`/rrhh/api/empleados/${empleadoId}/permisos?page=${pagina}`)
        .then(response => response.json())
        .then(data => {
            if (data.items.length === 0) {
                contenedor.innerHTML = '<div class="alert alert-info">No hay solicitudes de permiso</div>';
                return;
            }
            
            let html = `
                <div class="tabla-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Tipo</th>
                                <th>Motivo</th>
                                <th>Período</th>
                                <th>Días</th>
                                <th>Con Goce</th>
                                <th>Justificativo</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.items.forEach(p => {
                html += `
                    <tr>
                        <td>${p.tipo}</td>
                        <td>${p.motivo}</td>
                        <td>${p.fecha_inicio} a ${p.fecha_fin}</td>
                        <td>${p.dias}</td>
                                <td>${p.con_goce}</td>
                                <td>
                                    ${p.justificativo ? `<a href="/rrhh/${p.justificativo}" target="_blank" class="btn btn-sm btn-outline-primary">Ver</a>` : ''}
                                    <input type="file" id="perm-file-${p.id}" style="display:none" onchange="uploadPermisoJustificativo(${p.id})">
                                    <button class="btn btn-sm btn-secondary" onclick="document.getElementById('perm-file-${p.id}').click()">Subir</button>
                                </td>
                                <td><span class="badge bg-${p.estado === 'Aprobado' ? 'success' : (p.estado === 'Rechazado' ? 'danger' : 'warning')}">${p.estado}</span></td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            
            // Paginación
            if (data.pages > 1) {
                html += '<nav><ul class="pagination justify-content-center">';
                
                if (data.current_page > 1) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarPermisos(1)">Primera</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarPermisos(${data.current_page - 1})">Anterior</button></li>`;
                }
                
                html += `<li class="page-item active"><span class="page-link">${data.current_page} / ${data.pages}</span></li>`;
                
                if (data.current_page < data.pages) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarPermisos(${data.current_page + 1})">Siguiente</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarPermisos(${data.pages})">Última</button></li>`;
                }
                
                html += '</ul></nav>';
            }
            
            contenedor.innerHTML = html;
        })
        .catch(err => mostrarError(contenedor, 'Error al cargar permisos'));
}

// ========== TAB SANCIONES ==========
function cargarSanciones(pagina) {
    const contenedor = document.getElementById('sanciones-content');
    mostrarCarga(contenedor);
    
    fetch(`/rrhh/api/empleados/${empleadoId}/sanciones?page=${pagina}`)
        .then(response => response.json())
        .then(data => {
            if (data.items.length === 0) {
                contenedor.innerHTML = '<div class="alert alert-info">No hay sanciones registradas</div>';
                return;
            }
            
            let html = `
                <div class="tabla-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Tipo</th>
                                <th>Motivo</th>
                                <th>Monto</th>
                                <th>Fecha</th>
                                <th>Descripción</th>
                                        <th>Justificativo</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.items.forEach(s => {
                html += `
                    <tr>
                        <td><strong>${s.tipo}</strong></td>
                        <td>${s.motivo}</td>
                        <td>${formatearMoneda(s.monto)}</td>
                        <td>${s.fecha}</td>
                        <td>${s.descripcion}</td>
                        <td>
                            ${s.justificativo ? `<a href="/rrhh/${s.justificativo}" target="_blank" class="btn btn-sm btn-outline-primary">Ver</a>` : ''}
                            <input type="file" id="sanc-file-${s.id}" style="display:none" onchange="uploadSancionJustificativo(${s.id})">
                            <button class="btn btn-sm btn-secondary" onclick="document.getElementById('sanc-file-${s.id}').click()">Subir</button>
                        </td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            
            // Paginación
            if (data.pages > 1) {
                html += '<nav><ul class="pagination justify-content-center">';
                
                if (data.current_page > 1) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarSanciones(1)">Primera</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarSanciones(${data.current_page - 1})">Anterior</button></li>`;
                }
                
                html += `<li class="page-item active"><span class="page-link">${data.current_page} / ${data.pages}</span></li>`;
                
                if (data.current_page < data.pages) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarSanciones(${data.current_page + 1})">Siguiente</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarSanciones(${data.pages})">Última</button></li>`;
                }
                
                html += '</ul></nav>';
            }
            
            contenedor.innerHTML = html;
        })
        .catch(err => mostrarError(contenedor, 'Error al cargar sanciones'));
}

// ========== UPLOADS: Permisos / Sanciones ==========
function uploadPermisoJustificativo(permisoId) {
    const input = document.getElementById(`perm-file-${permisoId}`);
    if (!input || !input.files || input.files.length === 0) return;

    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch(`/rrhh/permisos/${permisoId}/upload-justificativo`, {
        method: 'POST',
        body: formData
    }).then(r => r.json())
      .then(resp => {
          if (resp.error) {
              alert('Error: ' + resp.error);
          } else {
              // recargar la lista de permisos
              cargarPermisos(1);
          }
      }).catch(err => alert('Error al subir archivo'));
}

function uploadSancionJustificativo(sancionId) {
    const input = document.getElementById(`sanc-file-${sancionId}`);
    if (!input || !input.files || input.files.length === 0) return;

    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch(`/rrhh/sanciones/${sancionId}/upload-justificativo`, {
        method: 'POST',
        body: formData
    }).then(r => r.json())
      .then(resp => {
          if (resp.error) {
              alert('Error: ' + resp.error);
          } else {
              // recargar la lista de sanciones
              cargarSanciones(1);
          }
      }).catch(err => alert('Error al subir archivo'));
}

// ========== TAB LIQUIDACIONES ==========
function cargarLiquidaciones(pagina) {
    const contenedor = document.getElementById('liquidaciones-content');
    mostrarCarga(contenedor);
    
    let url = `/rrhh/api/empleados/${empleadoId}/liquidaciones?page=${pagina}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.items.length === 0) {
                contenedor.innerHTML = '<div class="alert alert-info">No hay liquidaciones registradas</div>';
                return;
            }
            
            let html = `
                <div class="tabla-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Período</th>
                                <th>Salario Base</th>
                                <th>Ingresos Extras</th>
                                <th>Descuentos</th>
                                <th>Aporte IPS</th>
                                <th>Neto</th>
                                <th>Días</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.items.forEach(l => {
                html += `
                    <tr>
                        <td><strong>${l.periodo}</strong></td>
                        <td>${formatearMoneda(l.salario_base)}</td>
                        <td>${formatearMoneda(l.ingresos_extras)}</td>
                        <td>${formatearMoneda(l.descuentos)}</td>
                        <td>${formatearMoneda(l.aporte_ips)}</td>
                        <td><strong>${formatearMoneda(l.salario_neto)}</strong></td>
                        <td>${l.dias_trabajados}</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            
            // Paginación
            if (data.pages > 1) {
                html += '<nav><ul class="pagination justify-content-center">';
                
                if (data.current_page > 1) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarLiquidaciones(1)">Primera</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarLiquidaciones(${data.current_page - 1})">Anterior</button></li>`;
                }
                
                html += `<li class="page-item active"><span class="page-link">${data.current_page} / ${data.pages}</span></li>`;
                
                if (data.current_page < data.pages) {
                    html += `<li class="page-item"><button class="page-link" onclick="cargarLiquidaciones(${data.current_page + 1})">Siguiente</button></li>`;
                    html += `<li class="page-item"><button class="page-link" onclick="cargarLiquidaciones(${data.pages})">Última</button></li>`;
                }
                
                html += '</ul></nav>';
            }
            
            contenedor.innerHTML = html;
        })
        .catch(err => mostrarError(contenedor, 'Error al cargar liquidaciones'));
}
