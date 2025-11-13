/**
 * modales.js
 * Funciones auxiliares para mostrar modales de confirmación y notificaciones
 */

/**
 * Mostrar modal de confirmación
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje a mostrar
 * @param {function} onConfirm - Callback al confirmar
 * @param {string} textoConfirm - Texto del botón confirmar (por defecto: "Confirmar")
 * @param {string} textoCancelar - Texto del botón cancelar (por defecto: "Cancelar")
 */
function mostrarConfirmacion(titulo, mensaje, onConfirm, textoConfirm = "Confirmar", textoCancelar = "Cancelar") {
    // Crear el modal dinámicamente
    const modalId = 'confirmModalDinamico';
    let modal = document.getElementById(modalId);
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = modalId;
        modal.className = 'modal fade';
        modal.setAttribute('tabindex', '-1');
        document.body.appendChild(modal);
    }
    
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${titulo}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${mensaje}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">${textoCancelar}</button>
                    <button type="button" class="btn btn-primary" id="btnConfirmar">${textoConfirm}</button>
                </div>
            </div>
        </div>
    `;
    
    const bsModal = new bootstrap.Modal(modal);
    
    document.getElementById('btnConfirmar').addEventListener('click', function() {
        bsModal.hide();
        onConfirm();
    });
    
    bsModal.show();
}

/**
 * Mostrar modal de éxito
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje a mostrar
 * @param {function} onClose - Callback al cerrar (opcional)
 */
function mostrarExito(titulo, mensaje, onClose = null) {
    console.log('=== ENTRANDO EN mostrarExito ===');
    console.log('Parámetros recibidos:', {titulo, mensaje, callback: onClose ? 'presente' : 'null'});
    
    try {
        // Destruir modal anterior si existe
        const modalIdAnterior = 'exitoModalDinamico';
        const modalAnterior = document.getElementById(modalIdAnterior);
        if (modalAnterior) {
            console.log('Eliminando modal anterior');
            const bsModalAnterior = bootstrap.Modal.getInstance(modalAnterior);
            if (bsModalAnterior) {
                bsModalAnterior.dispose();
            }
            modalAnterior.remove();
        }

        // Crear nuevo modal
        const modal = document.createElement('div');
        modal.id = modalIdAnterior;
        modal.className = 'modal fade';
        modal.setAttribute('tabindex', '-1');
        
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title"><i class="bi bi-check-circle"></i> ${titulo}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${mensaje}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" id="btnCerrarExito" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        console.log('Modal HTML creado y añadido al DOM');
        
        const bsModal = new bootstrap.Modal(modal);
        console.log('Instancia de Bootstrap Modal creada');
        
        if (onClose) {
            console.log('Registrando callback para el botón cerrar');
            const btnCerrar = document.getElementById('btnCerrarExito');
            if (btnCerrar) {
                btnCerrar.addEventListener('click', function(e) {
                    console.log('CLIC EN BOTÓN CERRAR DETECTADO');
                    e.preventDefault();
                    bsModal.hide();
                    setTimeout(function() {
                        console.log('Ejecutando callback después de cerrar modal');
                        onClose();
                    }, 300);
                });
            } else {
                console.log('ERROR: No se encontró btnCerrarExito');
            }
        }
        
        console.log('Mostrando modal');
        bsModal.show();
        console.log('Modal mostrado correctamente');
    } catch (error) {
        console.error('ERROR en mostrarExito:', error);
    }
}

/**
 * Mostrar modal de error
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje de error
 * @param {function} onClose - Callback al cerrar (opcional)
 */
function mostrarError(titulo, mensaje, onClose = null) {
    const modalId = 'errorModalDinamico';
    let modal = document.getElementById(modalId);
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = modalId;
        modal.className = 'modal fade';
        modal.setAttribute('tabindex', '-1');
        document.body.appendChild(modal);
    }
    
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title"><i class="bi bi-exclamation-circle"></i> ${titulo}</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${mensaje}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cerrar</button>
                </div>
            </div>
        </div>
    `;
    
    const bsModal = new bootstrap.Modal(modal);
    
    if (onClose) {
        modal.addEventListener('hidden.bs.modal', onClose, { once: true });
    }
    
    bsModal.show();
}

/**
 * Mostrar modal de información
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje a mostrar
 * @param {function} onClose - Callback al cerrar (opcional)
 */
function mostrarInfo(titulo, mensaje, onClose = null) {
    const modalId = 'infoModalDinamico';
    let modal = document.getElementById(modalId);
    
    if (!modal) {
        modal = document.createElement('div');
        modal.id = modalId;
        modal.className = 'modal fade';
        modal.setAttribute('tabindex', '-1');
        document.body.appendChild(modal);
    }
    
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-info text-white">
                    <h5 class="modal-title"><i class="bi bi-info-circle"></i> ${titulo}</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${mensaje}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-info" data-bs-dismiss="modal">Cerrar</button>
                </div>
            </div>
        </div>
    `;
    
    const bsModal = new bootstrap.Modal(modal);
    
    if (onClose) {
        modal.addEventListener('hidden.bs.modal', onClose, { once: true });
    }
    
    bsModal.show();
}
