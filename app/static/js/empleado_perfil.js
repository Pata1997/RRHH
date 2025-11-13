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

function mostrarErrorEnContenedor(elemento, mensaje) {
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
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar datos generales'));
}

// Aprobar / Rechazar Ingreso Extra desde el perfil
// Usar modales personalizados para confirmación y actualizar la lista al confirmar
window.abrirConfirmAprobar = function(ingresoId) {
    console.log('abrirConfirmAprobar llamado con ID:', ingresoId);
    mostrarConfirmacion('Aprobar Ingreso Extra', '¿Confirma aprobar este ingreso extra?', function() {
        console.log('Usuario confirmó aprobar');
        fetch(`/rrhh/ingresos-extras/${ingresoId}/approve`, { method: 'POST', headers: { 'X-CSRFToken': csrfToken } })
            .then(r => {
                console.log('Respuesta recibida del servidor:', r.status);
                return r.json();
            })
            .then(resp => {
                console.log('Respuesta parseada:', resp);
                if (resp.error) {
                    console.log('Error en respuesta:', resp.error);
                    mostrarError('Error', resp.error);
                } else {
                    console.log('Aprobación exitosa');
                    // Actualizar fila en el DOM como fallback
                    try {
                        const row = document.querySelector(`tr[data-ingreso-id="${ingresoId}"]`);
                        if (row) {
                            const badge = row.querySelector('td span.badge');
                            if (badge) {
                                badge.className = 'badge bg-success';
                                badge.textContent = 'APROBADO';
                            }
                            const actionsTd = row.querySelectorAll('td')[4];
                            if (actionsTd) actionsTd.innerHTML = '';
                        }
                    } catch (e) {
                        console.warn('No se pudo actualizar fila en DOM:', e);
                    }
                    // Recargar la tabla inmediatamente
                    console.log('RECARGANDO TABLA AHORA');
                    cargarIngresosExtras(window.ingresosCurrentPage || 1);
                    // Mostrar modal de éxito después de refrescar
                    setTimeout(function() {
                        console.log('Mostrando modal de éxito');
                        mostrarExito('Aprobado', 'Ingreso extra aprobado correctamente');
                    }, 100);
                }
            }).catch(err => {
                console.log('Error en fetch:', err);
                showFetchError(err);
            });
    }, 'Sí, aprobar', 'Cancelar');
}

window.abrirConfirmRechazar = function(ingresoId) {
    console.log('abrirConfirmRechazar llamado con ID:', ingresoId);
    mostrarConfirmacion('Rechazar Ingreso Extra', '¿Confirma rechazar este ingreso extra?', function() {
        console.log('Usuario confirmó rechazar');
        fetch(`/rrhh/ingresos-extras/${ingresoId}/reject`, { method: 'POST', headers: { 'X-CSRFToken': csrfToken } })
            .then(r => {
                console.log('Respuesta recibida del servidor:', r.status);
                return r.json();
            })
            .then(resp => {
                console.log('Respuesta parseada:', resp);
                if (resp.error) {
                    console.log('Error en respuesta:', resp.error);
                    mostrarError('Error', resp.error);
                } else {
                    console.log('Rechazo exitoso');
                    // Actualizar fila en el DOM como fallback
                    try {
                        const row = document.querySelector(`tr[data-ingreso-id="${ingresoId}"]`);
                        if (row) {
                            const badge = row.querySelector('td span.badge');
                            if (badge) {
                                badge.className = 'badge bg-danger';
                                badge.textContent = 'RECHAZADO';
                            }
                            const actionsTd = row.querySelectorAll('td')[4];
                            if (actionsTd) actionsTd.innerHTML = '';
                        }
                    } catch (e) {
                        console.warn('No se pudo actualizar fila en DOM:', e);
                    }
                    // Recargar la tabla inmediatamente
                    console.log('RECARGANDO TABLA AHORA');
                    cargarIngresosExtras(window.ingresosCurrentPage || 1);
                    // Mostrar modal de éxito después de refrescar
                    setTimeout(function() {
                        console.log('Mostrando modal de éxito');
                        mostrarExito('Rechazado', 'Ingreso extra rechazado correctamente');
                    }, 100);
                }
            }).catch(err => {
                console.log('Error en fetch:', err);
                showFetchError(err);
            });
    }, 'Sí, rechazar', 'Cancelar');
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
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar asistencias'));
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
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar vacaciones'));
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
                                    ${p.justificativo ? `<a href="/rrhh/${p.justificativo}" download class="btn btn-sm btn-outline-success">Descargar</a>` : ''}
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
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar permisos'));
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
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar sanciones'));
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
                                <th>Salario Neto</th>
                                <th>Días Trabajados</th>
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
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar liquidaciones'));
}

// ========== TAB ANTICIPOS ==========
function cargarAnticipos(pagina) {
    const contenedor = document.getElementById('anticipos-content');
    if (!contenedor) return;
    mostrarCarga(contenedor);

    fetch(`/rrhh/api/empleados/${empleadoId}/anticipos?page=${pagina}`)
        .then(r => r.json())
        .then(data => {
            let html = `
                <div class="mb-4">
                    <div class="card">
                        <div class="card-header bg-light">
                            <h6 class="mb-0"><i class="bi bi-plus-circle"></i> Solicitar Nuevo Adelanto</h6>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Monto (₲)</label>
                                        <input type="number" id="anticipos-monto" class="form-control" placeholder="500000" min="1">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">Observaciones (opcional)</label>
                                        <input type="text" id="anticipos-obs" class="form-control" placeholder="Motivo del adelanto">
                                    </div>
                                </div>
                            </div>
                            <button class="btn btn-primary" onclick="crearAnticipo()">
                                <i class="bi bi-send"></i> Solicitar Adelanto
                            </button>
                        </div>
                    </div>
                </div>
            `;

            if (data.items.length === 0) {
                html += '<div class="alert alert-info">No hay anticipos registrados</div>';
            } else {
                html += `
                    <div class="tabla-responsive">
                        <table class="table table-sm table-hover">
                            <thead>
                                <tr>
                                    <th>Monto</th>
                                    <th>Fecha</th>
                                    <th>Estado</th>
                                    <th>Justificativo</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                data.items.forEach(a => {
                    let estadoBadge = '';
                    if (a.aprobado) {
                        estadoBadge = '<span class="badge bg-success">Aprobado</span>';
                    } else if (a.rechazado) {
                        estadoBadge = '<span class="badge bg-danger">Rechazado</span>';
                    } else {
                        estadoBadge = '<span class="badge bg-warning">Pendiente</span>';
                    }
                    
                    html += `
                        <tr>
                            <td>${formatearMoneda(a.monto)}</td>
                            <td>${a.fecha_solicitud}</td>
                            <td>${estadoBadge}</td>
                            <td>${a.justificativo ? `<a href="/rrhh/uploads/${a.justificativo}" download class="btn btn-sm btn-outline-success">Descargar</a>` : ''}</td>
                            <td>
                                ${!a.aprobado && !a.rechazado && isRRHH ? `
                                    <button class="btn btn-sm btn-success" onclick="aprobarAnticipo(${a.id})"><i class="bi bi-check"></i> Aprobar</button>
                                    <button class="btn btn-sm btn-danger" onclick="rechazarAnticipo(${a.id})"><i class="bi bi-x"></i> Rechazar</button>
                                ` : ''}
                                <input type="file" id="antic-file-${a.id}" style="display:none" onchange="uploadAnticipoJustificativo(${a.id})">
                                <button class="btn btn-sm btn-secondary" onclick="document.getElementById('antic-file-${a.id}').click()"><i class="bi bi-upload"></i> Subir</button>
                            </td>
                        </tr>
                    `;
                });

                html += '</tbody></table></div>';
            }

            contenedor.innerHTML = html;
        })
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar anticipos'));
}


// ========== TAB INGRESOS EXTRAS (en perfil) ==========
function cargarIngresosExtras(pagina) {
    console.log('cargarIngresosExtras llamado con pagina:', pagina);
    const contenedor = document.getElementById('ingresos-extras-content');
    console.log('Contenedor encontrado:', contenedor ? 'Sí' : 'No');
    if (!contenedor) return;
    mostrarCarga(contenedor);

    const per_page = 10;
    window.ingresosCurrentPage = pagina || 1;
    console.log('Haciendo fetch a:', `/rrhh/api/empleados/${empleadoId}/ingresos-extras?page=${window.ingresosCurrentPage}&per_page=${per_page}`);
    fetch(`/rrhh/api/empleados/${empleadoId}/ingresos-extras?page=${window.ingresosCurrentPage}&per_page=${per_page}`)
        .then(r => {
            console.log('Respuesta del API:', r.status);
            return r.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            if (!data.items || data.items.length === 0) {
                console.log('No hay items en la respuesta');
                contenedor.innerHTML = '<div class="alert alert-info">No hay Ingresos Extras registrados</div>';
                return;
            }

            let html = `
                <div class="table-responsive">
                    <table class="table table-sm table-hover">
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Tipo</th>
                                <th>Monto</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            data.items.forEach(it => {
                const estado = it.estado || '';
                const badge = estado === 'APROBADO' ? 'success' : (estado === 'RECHAZADO' ? 'danger' : 'warning');
                html += `
                    <tr data-ingreso-id="${it.id}">
                        <td>${it.fecha_creacion || '-'}</td>
                        <td>${it.tipo || '-'}</td>
                        <td>${it.monto ? formatearMoneda(it.monto) : '-'}</td>
                        <td><span class="badge bg-${badge}">${estado}</span></td>
                        <td>` + (estado === 'PENDIENTE' && typeof isRRHH !== 'undefined' && isRRHH ? `
                                <button class="btn btn-sm btn-success" onclick="abrirConfirmAprobar(${it.id})">Aprobar</button>
                                <button class="btn btn-sm btn-danger" onclick="abrirConfirmRechazar(${it.id})">Rechazar</button>
                            ` : '') + `</td>
                    </tr>`;
            });

            html += `</tbody></table></div>`;

            // paginación simple
            if (data.pages > 1) {
                html += '<nav><ul class="pagination justify-content-center">';
                if (data.page > 1) html += `<li class="page-item"><button class="page-link" onclick="cargarIngresosExtras(1)">Primera</button></li>`;
                if (data.page > 1) html += `<li class="page-item"><button class="page-link" onclick="cargarIngresosExtras(${data.page - 1})">Anterior</button></li>`;
                html += `<li class="page-item active"><span class="page-link">${data.page} / ${data.pages}</span></li>`;
                if (data.page < data.pages) html += `<li class="page-item"><button class="page-link" onclick="cargarIngresosExtras(${data.page + 1})">Siguiente</button></li>`;
                if (data.page < data.pages) html += `<li class="page-item"><button class="page-link" onclick="cargarIngresosExtras(${data.pages})">Última</button></li>`;
                html += '</ul></nav>';
            }

            contenedor.innerHTML = html;
        })
        .catch(err => mostrarErrorEnContenedor(contenedor, 'Error al cargar Ingresos Extras'));
}

function showFetchError(err) {
    console.error(err);
    mostrarError('Error', err.message || 'Error en la comunicación con el servidor');
}

function crearAnticipo() {
    const monto = document.getElementById('anticipos-monto').value;
    const obs = document.getElementById('anticipos-obs').value;

    if (!monto || monto <= 0) {
        mostrarError('Validación', 'Por favor ingresa un monto válido');
        return;
    }

    fetch(`/rrhh/anticipos/create`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            empleado_id: empleadoId,
            monto: parseFloat(monto),
            observaciones: obs || null
        })
    }).then(r => r.json())
      .then(resp => {
          if (resp.error) {
              mostrarError('Error', resp.error);
          } else {
              document.getElementById('anticipos-monto').value = '';
              document.getElementById('anticipos-obs').value = '';
              mostrarExito('Éxito', 'Anticipo solicitado correctamente');
              setTimeout(() => cargarAnticipos(1), 1000);
          }
      }).catch(err => {
          mostrarError('Error', 'Error al crear anticipo: ' + err.message);
      });
}



function uploadAnticipoJustificativo(anticipoId) {
    const input = document.getElementById('antic-file-' + anticipoId);
    if (!input || !input.files || input.files.length === 0) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch(`/rrhh/anticipos/${anticipoId}/upload-justificativo`, {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrfToken }
    }).then(r => r.json())
      .then(resp => {
          if (resp.error) {
              mostrarError('Error', resp.error);
          } else {
              mostrarExito('Éxito', 'Justificativo subido correctamente');
              setTimeout(() => cargarAnticipos(1), 500);
          }
      }).catch(err => {
          mostrarError('Error', 'Error al subir archivo: ' + err.message);
      });
}

function aprobarAnticipo(anticipoId) {
    mostrarConfirmacion(
        'Aprobar Anticipo',
        '¿Estás seguro de que deseas aprobar este anticipo y generar el recibo PDF?',
        function() {
            fetch(`/rrhh/anticipos/${anticipoId}/approve`, { 
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(r => r.json())
            .then(resp => {
                if (resp.error) {
                    mostrarError('Error', resp.error);
                } else {
                    // Descargar el PDF automáticamente
                    if (resp.ruta_pdf) {
                        const link = document.createElement('a');
                        link.href = `/rrhh/uploads/${resp.ruta_pdf}`;
                        link.download = resp.ruta_pdf.split('/').pop();
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }
                    
                    mostrarExito('Éxito', 'Anticipo aprobado correctamente. PDF generado y descargado.');
                    // Recargar después de 1 segundo
                    setTimeout(() => cargarAnticipos(1), 1000);
                }
            }).catch(err => {
                mostrarError('Error', 'Error al aprobar anticipo: ' + err.message);
            });
        },
        'Sí, Aprobar',
        'Cancelar'
    );
}

function rechazarAnticipo(anticipoId) {
    mostrarConfirmacion(
        'Rechazar Anticipo',
        '¿Estás seguro de que deseas rechazar este anticipo?',
        function() {
            fetch(`/rrhh/anticipos/${anticipoId}/reject`, { 
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(r => r.json())
            .then(resp => {
                if (resp.error) {
                    mostrarError('Error', resp.error);
                } else {
                    mostrarExito('Éxito', 'Anticipo rechazado correctamente.');
                    // Recargar después de 1 segundo
                    setTimeout(() => cargarAnticipos(1), 1000);
                }
            }).catch(err => {
                mostrarError('Error', 'Error al rechazar anticipo: ' + err.message);
            });
        },
        'Sí, Rechazar',
        'Cancelar'
    );
}

// Hook para cargar anticipos cuando se muestra la pestaña (si existe)
document.getElementById('anticipos-tab') && document.getElementById('anticipos-tab').addEventListener('shown.bs.tab', function() {
    cargarAnticipos(1);
});
