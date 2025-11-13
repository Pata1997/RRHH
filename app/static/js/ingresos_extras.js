document.addEventListener('DOMContentLoaded', function() {
    const btnCargar = document.getElementById('btn-cargar');
    const periodoInput = document.getElementById('periodo-input');

    function cargarEmpleados() {
        const periodo = periodoInput.value;
        fetch(`/rrhh/api/ingresos-extras/employees?periodo=${periodo}`)
            .then(r => r.json())
            .then(data => renderEmpleados(data.items, data.periodo))
            .catch(err => console.error(err));
    }

    function renderEmpleados(items, periodo) {
        const cont = document.getElementById('empleados-list');
        if (!items || items.length === 0) {
            cont.innerHTML = '<div class="alert alert-info">No hay empleados.</div>';
            return;
        }

        let html = '<div class="table-responsive"><table class="table table-sm table-hover"><thead><tr><th>Empleado</th><th>Pendientes</th><th>Total Horas</th><th>Acciones</th></tr></thead><tbody>';
        items.forEach(it => {
            html += `<tr>
                <td>${it.nombre}</td>
                <td>${it.pendientes}</td>
                <td>${it.total_horas}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="verHoras(${it.id}, '${periodo}')">Ver Horas Extra</button>
                    <a class="btn btn-sm btn-secondary" href="/rrhh/ingresos-extras/create?empleado_id=${it.id}">Ingreso Extra</a>
                </td>
            </tr>`;
        });
        html += '</tbody></table></div>';
        cont.innerHTML = html;
    }

    window.verHoras = function(empleadoId, periodo) {
        fetch(`/rrhh/api/empleados/${empleadoId}/horas-extras?periodo=${periodo}`)
            .then(r => r.json())
            .then(data => {
                const modalTitle = document.getElementById('modalHorasTitle');
                modalTitle.textContent = `Horas Extra - ${data.empleado} (${data.periodo})`;
                const body = document.getElementById('modalHorasBody');
                if (!data.items || data.items.length === 0) {
                    body.innerHTML = '<div class="alert alert-info">No hay horas extra detectadas para este período.</div>';
                } else {
                    let html = '<div class="table-responsive"><table class="table table-sm"><thead><tr><th>Fecha</th><th>Horas</th><th>Monto</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>';
                    data.items.forEach(h => {
                        html += `<tr>
                            <td>${h.fecha}</td>
                            <td>${h.horas}</td>
                            <td>Gs. ${h.monto.toLocaleString()}</td>
                            <td>${h.estado}</td>
                            <td>`;
                        if (h.estado === 'PENDIENTE') {
                            html += `<button class="btn btn-sm btn-success" onclick="aprobarHora(${h.id})">Aprobar</button> `;
                            html += `<button class="btn btn-sm btn-danger" onclick="rechazarHora(${h.id})">Rechazar</button>`;
                        }
                        html += `</td></tr>`;
                    });
                    html += '</tbody></table></div>';
                    body.innerHTML = html;
                }

                var modal = new bootstrap.Modal(document.getElementById('modalHoras'));
                modal.show();
            })
            .catch(err => console.error(err));
    }

    window.aprobarHora = function(horaId) {
        fetch(`/rrhh/horas-extra/${horaId}/approve`, { method: 'POST' })
            .then(r => r.json())
            .then(resp => {
                if (resp.error) alert('Error: ' + resp.error);
                else {
                    alert('Hora aprobada');
                    // recargar modal/tabla
                    document.getElementById('btn-cargar').click();
                }
            }).catch(err => alert('Error: ' + err.message));
    }

    window.rechazarHora = function(horaId) {
        fetch(`/rrhh/horas-extra/${horaId}/reject`, { method: 'POST' })
            .then(r => r.json())
            .then(resp => {
                if (resp.error) alert('Error: ' + resp.error);
                else {
                    alert('Hora rechazada');
                    document.getElementById('btn-cargar').click();
                }
            }).catch(err => alert('Error: ' + err.message));
    }

    btnCargar.addEventListener('click', cargarEmpleados);
    // cargar al inicio
    cargarEmpleados();
});
