from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from sqlalchemy import func, desc, or_
from decimal import Decimal
from datetime import datetime, date, timedelta
import calendar
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json
import os
from werkzeug.utils import secure_filename
from io import BytesIO

from ..models import (
    db, Empleado, Cargo, Asistencia, Permiso, Sancion, 
    Contrato, Liquidacion, Vacacion, IngresoExtra, Descuento, 
    Bitacora, EstadoEmpleadoEnum, EstadoVacacionEnum, EstadoPermisoEnum, RoleEnum, Despido,
    Postulante, DocumentosCurriculum, AsistenciaEvento
)
from ..bitacora import registrar_bitacora, registrar_operacion_crud
from ..reports.report_utils import ReportUtils

rrhh_bp = Blueprint('rrhh', __name__, url_prefix='/rrhh')

from functools import wraps

# Decorador para verificar rol
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.rol not in roles:
                flash('No tienes permiso para acceder a este módulo', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Configuraciones de uploads
UPLOADS_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
PERMISOS_UPLOAD_FOLDER = os.path.join(UPLOADS_ROOT, 'permisos')
SANCIONES_UPLOAD_FOLDER = os.path.join(UPLOADS_ROOT, 'sanciones')
POSTULANTES_UPLOAD_FOLDER = os.path.join(UPLOADS_ROOT, 'postulantes')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Servir archivos subidos (permisos/sanciones/postulantes)
@rrhh_bp.route('/uploads/<path:subpath>')
@login_required
def serve_uploads(subpath):
    base = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(base, subpath)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath)

# ==================== EMPLEADOS ====================
@rrhh_bp.route('/empleados', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def listar_empleados():
    """Lista todos los empleados"""
    registrar_bitacora(current_user, 'empleados', 'VIEW', 'empleados')
    
    pagina = request.args.get('page', 1, type=int)
    empleados = Empleado.query.paginate(page=pagina, per_page=10)
    
    return render_template('rrhh/empleados.html', empleados=empleados)

@rrhh_bp.route('/empleados/crear', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def crear_empleado():
    """Crear nuevo empleado"""
    cargos = Cargo.query.all()
    
    if request.method == 'POST':
        try:
            # Validar datos
            codigo = request.form.get('codigo')
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            ci = request.form.get('ci')
            cargo_id = request.form.get('cargo_id')
            salario_base = request.form.get('salario_base')
            fecha_ingreso = datetime.strptime(request.form.get('fecha_ingreso'), '%Y-%m-%d').date()
            
            # Verificar que no exista
            if Empleado.query.filter_by(codigo=codigo).first():
                flash('El código del empleado ya existe', 'danger')
                return redirect(url_for('rrhh.crear_empleado'))
            
            if Empleado.query.filter_by(ci=ci).first():
                flash('El CI ya existe en el sistema', 'danger')
                return redirect(url_for('rrhh.crear_empleado'))
            
            # Crear empleado
            empleado = Empleado(
                codigo=codigo,
                nombre=nombre,
                apellido=apellido,
                ci=ci,
                cargo_id=int(cargo_id),
                salario_base=Decimal(salario_base),
                fecha_ingreso=fecha_ingreso,
                email=request.form.get('email'),
                telefono=request.form.get('telefono'),
                direccion=request.form.get('direccion'),
                sexo=request.form.get('sexo'),
                fecha_nacimiento=request.form.get('fecha_nacimiento') and datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d').date()
            )
            
            db.session.add(empleado)
            db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'empleados', 'CREATE', 'empleados', 
                empleado.id, {'codigo': codigo, 'nombre': nombre, 'apellido': apellido}
            )
            
            flash(f'Empleado {empleado.nombre_completo} creado exitosamente', 'success')
            return redirect(url_for('rrhh.listar_empleados'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear empleado: {str(e)}', 'danger')
    
    return render_template('rrhh/crear_empleado.html', cargos=cargos)

@rrhh_bp.route('/empleados/<int:empleado_id>/editar', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def editar_empleado(empleado_id):
    """Editar empleado"""
    empleado = Empleado.query.get_or_404(empleado_id)
    cargos = Cargo.query.all()
    
    if request.method == 'POST':
        try:
            empleado.nombre = request.form.get('nombre')
            empleado.apellido = request.form.get('apellido')
            empleado.cargo_id = int(request.form.get('cargo_id'))
            empleado.salario_base = Decimal(request.form.get('salario_base'))
            empleado.email = request.form.get('email')
            empleado.telefono = request.form.get('telefono')
            empleado.direccion = request.form.get('direccion')
            empleado.sexo = request.form.get('sexo')
            empleado.estado = EstadoEmpleadoEnum[request.form.get('estado')]
            
            fecha_nacimiento_str = request.form.get('fecha_nacimiento')
            if fecha_nacimiento_str:
                empleado.fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
            
            db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'empleados', 'UPDATE', 'empleados', 
                empleado_id, {'cambios': 'Datos del empleado actualizados'}
            )
            
            flash(f'Empleado {empleado.nombre_completo} actualizado exitosamente', 'success')
            return redirect(url_for('rrhh.listar_empleados'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar empleado: {str(e)}', 'danger')
    
    return render_template('rrhh/editar_empleado.html', empleado=empleado, cargos=cargos)

@rrhh_bp.route('/empleados/<int:empleado_id>/eliminar', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def eliminar_empleado(empleado_id):
    """Eliminar empleado (solo RRHH)"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    try:
        codigo = empleado.codigo
        db.session.delete(empleado)
        db.session.commit()
        
        registrar_operacion_crud(
            current_user, 'empleados', 'DELETE', 'empleados', 
            empleado_id, {'codigo': codigo}
        )
        
        flash('Empleado eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar empleado: {str(e)}', 'danger')
    
    return redirect(url_for('rrhh.listar_empleados'))

# ==================== CARGOS ====================
@rrhh_bp.route('/cargos', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def listar_cargos():
    """Lista todos los cargos"""
    registrar_bitacora(current_user, 'cargos', 'VIEW', 'cargos')
    cargos = Cargo.query.all()
    return render_template('rrhh/cargos.html', cargos=cargos)

@rrhh_bp.route('/cargos/crear', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def crear_cargo():
    """Crear nuevo cargo"""
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            
            if Cargo.query.filter_by(nombre=nombre).first():
                flash('El cargo ya existe', 'danger')
                return redirect(url_for('rrhh.crear_cargo'))
            
            cargo = Cargo(
                nombre=nombre,
                descripcion=request.form.get('descripcion'),
                salario_base=Decimal(request.form.get('salario_base'))
            )
            
            db.session.add(cargo)
            db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'cargos', 'CREATE', 'cargos', 
                cargo.id, {'nombre': nombre}
            )
            
            flash(f'Cargo {cargo.nombre} creado exitosamente', 'success')
            return redirect(url_for('rrhh.listar_cargos'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cargo: {str(e)}', 'danger')
    
    return render_template('rrhh/crear_cargo.html')

@rrhh_bp.route('/cargos/<int:cargo_id>/editar', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def editar_cargo(cargo_id):
    """Editar cargo"""
    cargo = Cargo.query.get_or_404(cargo_id)
    
    if request.method == 'POST':
        try:
            cargo.nombre = request.form.get('nombre')
            cargo.descripcion = request.form.get('descripcion')
            cargo.salario_base = Decimal(request.form.get('salario_base'))
            
            db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'cargos', 'UPDATE', 'cargos', 
                cargo_id, {'cambios': 'Datos del cargo actualizados'}
            )
            
            flash(f'Cargo {cargo.nombre} actualizado exitosamente', 'success')
            return redirect(url_for('rrhh.listar_cargos'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cargo: {str(e)}', 'danger')
    
    return render_template('rrhh/editar_cargo.html', cargo=cargo)

@rrhh_bp.route('/cargos/<int:cargo_id>/eliminar', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def eliminar_cargo(cargo_id):
    """Eliminar cargo"""
    cargo = Cargo.query.get_or_404(cargo_id)
    
    # Verificar si hay empleados con este cargo
    if cargo.empleados:
        flash('No se puede eliminar un cargo que tiene empleados asignados', 'danger')
        return redirect(url_for('rrhh.listar_cargos'))
    
    try:
        nombre = cargo.nombre
        db.session.delete(cargo)
        db.session.commit()
        
        registrar_operacion_crud(
            current_user, 'cargos', 'DELETE', 'cargos', 
            cargo_id, {'nombre': nombre}
        )
        
        flash('Cargo eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cargo: {str(e)}', 'danger')
    
    return redirect(url_for('rrhh.listar_cargos'))

# ==================== ASISTENCIA ====================
@rrhh_bp.route('/asistencia', methods=['GET'])
@login_required
def ver_asistencia():
    """Vista de asistencia para registrar entrada/salida"""
    registrar_bitacora(current_user, 'asistencia', 'VIEW', 'asistencias')
    
    pagina = request.args.get('page', 1, type=int)
    fecha_filtro = request.args.get('fecha', str(date.today()))
    
    try:
        fecha_date = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
    except:
        fecha_date = date.today()
    
    asistencias = Asistencia.query.filter_by(fecha=fecha_date).paginate(page=pagina, per_page=20)
    
    return render_template('rrhh/asistencia.html', asistencias=asistencias, fecha=fecha_filtro)


def _parse_time(cfg_key, default='08:30'):
    s = current_app.config.get(cfg_key, default)
    try:
        return datetime.strptime(s, '%H:%M').time()
    except Exception:
        return datetime.strptime(default, '%H:%M').time()


def _resumir_dia_asistencias(empleado_id, dia_date):
    """Resumir los eventos del día y devolver dict con hora_entrada, hora_salida, presente, observaciones"""
    eventos = AsistenciaEvento.query.filter(
        AsistenciaEvento.empleado_id == empleado_id,
        func.date(AsistenciaEvento.ts) == dia_date
    ).order_by(AsistenciaEvento.ts).all()

    on_time = _parse_time('ASISTENCIA_ON_TIME', '08:30')
    tolerancia = _parse_time('ASISTENCIA_TOLERANCE', '08:50')
    corte_manana = _parse_time('ASISTENCIA_CORTE_MANANA', '12:00')
    inicio_tarde = _parse_time('ASISTENCIA_INICIO_TARDE', '13:30')
    salida_final = _parse_time('ASISTENCIA_SALIDA_FINAL', '16:00')

    primera_entrada = None
    ultima_salida = None
    observaciones = []

    # Encontrar primera entrada y última salida
    for ev in eventos:
        if ev.tipo == 'in' and primera_entrada is None:
            primera_entrada = ev.ts
        if ev.tipo == 'out':
            ultima_salida = ev.ts

    # Clasificar llegada
    if primera_entrada:
        t = primera_entrada.time()
        if t <= on_time:
            observaciones.append('A tiempo')
        elif t <= tolerancia:
            observaciones.append('Tolerancia')
        elif t < corte_manana:
            observaciones.append('Llegada tardía')
        else:
            # Entrada después del corte de mañana -> considerarla llegada tarde o sólo tarde
            if t >= inicio_tarde:
                observaciones.append('Solo tarde')
            else:
                observaciones.append('Llegada tardía')
    else:
        # No hay entrada por la mañana
        # Si existe entrada por la tarde, marcar solo tarde
        entrada_tarde = next((ev for ev in eventos if ev.tipo == 'in' and ev.ts.time() >= inicio_tarde), None)
        if entrada_tarde:
            observaciones.append('Ausente mañana; Solo tarde')
            primera_entrada = entrada_tarde.ts if hasattr(entrada_tarde, 'ts') else entrada_tarde.ts
        else:
            observaciones.append('Ausencia')

    # Detectar salida al almuerzo (primer out cercano a medio día)
    lunch_out = next((ev for ev in eventos if ev.tipo == 'out' and ev.ts.time() >= (datetime.strptime('11:30','%H:%M').time()) and ev.ts.time() <= (datetime.strptime('13:30','%H:%M').time())), None)
    if lunch_out:
        observaciones.append('Salida al almuerzo')
        # buscar entrada después del almuerzo
        lunch_in = next((ev for ev in eventos if ev.tipo == 'in' and ev.ts > lunch_out.ts), None)
        if lunch_in:
            observaciones.append('Entrada del almuerzo')

    # Clasificar salida final
    if ultima_salida:
        if ultima_salida.time() >= salida_final:
            observaciones.append('Salida final')
        else:
            observaciones.append('Salida temprana')

    resumen = {
        'hora_entrada': primera_entrada.time() if primera_entrada else None,
        'hora_salida': ultima_salida.time() if ultima_salida else None,
        'presente': True if eventos else False,
        'observaciones': '; '.join(observaciones) if observaciones else None
    }
    return resumen

@rrhh_bp.route('/asistencia/registrar', methods=['POST'])
@login_required
def registrar_asistencia():
    """Registra un evento de asistencia (punch) y actualiza el resumen diario."""
    try:
        codigo = request.json.get('codigo', '').strip().upper()
        if not codigo:
            return jsonify({'success': False, 'message': 'Código de empleado requerido'}), 400

        empleado = Empleado.query.filter_by(codigo=codigo).first()
        if not empleado:
            return jsonify({'success': False, 'message': f'Empleado con código {codigo} no encontrado'}), 404

        if empleado.estado.name != 'ACTIVO':
            return jsonify({'success': False, 'message': f'El empleado está {empleado.estado.value}'}), 403

        ahora = datetime.now()
        hoy = date.today()

        # Inferir tipo si no se pasa explícitamente
        tipo = request.json.get('tipo')
        eventos_count = AsistenciaEvento.query.filter(
            AsistenciaEvento.empleado_id == empleado.id,
            func.date(AsistenciaEvento.ts) == hoy
        ).count()
        if tipo not in ('in', 'out'):
            tipo = 'in' if eventos_count % 2 == 0 else 'out'

        evento = AsistenciaEvento(
            empleado_id=empleado.id,
            ts=ahora,
            tipo=tipo,
            origen=request.json.get('origen', 'web'),
            metadata=json.dumps({'ip': request.remote_addr, 'user_agent': request.headers.get('User-Agent')})
        )
        db.session.add(evento)
        db.session.commit()

        # Recalcular y almacenar resumen diario
        resumen = _resumir_dia_asistencias(empleado.id, hoy)

        asistencia = Asistencia.query.filter_by(empleado_id=empleado.id, fecha=hoy).first()
        if not asistencia:
            asistencia = Asistencia(empleado_id=empleado.id, fecha=hoy)
            db.session.add(asistencia)

        asistencia.hora_entrada = resumen.get('hora_entrada')
        asistencia.hora_salida = resumen.get('hora_salida')
        asistencia.presente = resumen.get('presente', True)
        asistencia.observaciones = resumen.get('observaciones')
        db.session.commit()

        registrar_operacion_crud(current_user, 'asistencia', 'CREATE', 'asistencias', asistencia.id, {'empleado_codigo': codigo, 'evento_id': evento.id, 'tipo_evento': tipo})

        return jsonify({'success': True, 'message': f'Evento {tipo} registrado para {empleado.nombre_completo}', 'tipo': tipo, 'hora': ahora.strftime('%H:%M:%S'), 'resumen': resumen})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
@rrhh_bp.route('/permisos/empleado/<int:empleado_id>', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def ver_historial_permisos(empleado_id):
    """Ver historial de permisos de un empleado, incluyendo observaciones"""
    registrar_bitacora(current_user, 'permisos', 'VIEW', 'permisos')

    empleado = Empleado.query.get_or_404(empleado_id)
    permisos = Permiso.query.filter_by(empleado_id=empleado_id).order_by(Permiso.fecha_creacion.desc()).all()
    pendientes = [p for p in permisos if p.estado.name == 'PENDIENTE']

    return render_template('rrhh/permiso_detalle.html', empleado=empleado, permisos=permisos, pendientes=pendientes)

@rrhh_bp.route('/permisos/solicitar', methods=['GET', 'POST'])
@login_required
def solicitar_permiso():
    """Solicitar permiso"""
    empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
    
    if request.method == 'POST':
        try:
            fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%d').date()
            dias = (fecha_fin - fecha_inicio).days + 1

            # Validación mínima: exigir al menos 1 día
            if dias < 1:
                flash('El permiso debe incluir al menos un día', 'danger')
                return redirect(url_for('rrhh.solicitar_permiso'))
            # Determinar si el permiso es con goce salarial (checkbox en el form)
            con_goce_field = request.form.get('con_goce')
            con_goce = False
            if con_goce_field in ('on', 'true', '1', 'True'):
                con_goce = True

            permiso = Permiso(
                empleado_id=int(request.form.get('empleado_id')),
                tipo_permiso=request.form.get('tipo_permiso'),
                motivo=request.form.get('motivo'),
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                dias_solicitados=dias,
                observaciones=request.form.get('observaciones'),
                con_goce=con_goce
            )
            
            db.session.add(permiso)
            db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'permisos', 'CREATE', 'permisos',
                permiso.id, {'empleado_id': permiso.empleado_id, 'tipo': permiso.tipo_permiso}
            )
            
            flash('Permiso solicitado exitosamente', 'success')
            return redirect(url_for('rrhh.listar_permisos'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al solicitar permiso: {str(e)}', 'danger')
    
    return render_template('rrhh/solicitar_permiso.html', empleados=empleados)

@rrhh_bp.route('/permisos/<int:permiso_id>/aprobar', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def aprobar_permiso(permiso_id):
    """Aprobar permiso"""
    permiso = Permiso.query.get_or_404(permiso_id)
    
    try:
        from ..models import EstadoPermisoEnum, Descuento
        from decimal import Decimal

        permiso.estado = EstadoPermisoEnum.APROBADO

        # Si el permiso es SIN GOCE (con_goce == False), crear Descuento(s) automáticos por mes
        # (dividir si cruza meses) solo si no hay descuentos activos ya creados para este permiso.
        if not permiso.con_goce:
            existing = Descuento.query.filter_by(origen_tipo='permiso', origen_id=permiso.id, activo=True).count()
            if existing:
                # ya existen descuentos activos para este permiso, no crear duplicados
                db.session.commit()
                registrar_operacion_crud(
                    current_user, 'permisos', 'UPDATE', 'permisos',
                    permiso_id, {'estado': 'APROBADO', 'info': 'descuentos_existentes'}
                )
                flash('Permiso aprobado (descuentos ya creados anteriormente)', 'success')
                return redirect(url_for('rrhh.listar_permisos'))
            empleado = permiso.empleado
            salario = Decimal(empleado.salario_base)

            fecha_start = permiso.fecha_inicio
            fecha_end = permiso.fecha_fin

            descuentos_creados = []

            # Iterar por segmentos por mes
            current = fecha_start
            while current <= fecha_end:
                last_day = calendar.monthrange(current.year, current.month)[1]
                end_of_month = date(current.year, current.month, last_day)
                segment_end = end_of_month if end_of_month <= fecha_end else fecha_end

                dias_segment = (segment_end - current).days + 1
                monto_segment = (salario / Decimal('30')) * Decimal(dias_segment)
                monto_segment = monto_segment.quantize(Decimal('0.01'))

                desc = Descuento(
                    empleado_id=empleado.id,
                    tipo='Permiso sin goce',
                    monto=monto_segment,
                    mes=current.month,
                    año=current.year,
                    descripcion=f'Descuento automático por permiso id {permiso.id} ({current.strftime("%Y-%m")})',
                    activo=True,
                    origen_tipo='permiso',
                    origen_id=permiso.id
                )
                db.session.add(desc)
                db.session.flush()
                descuentos_creados.append(desc.id)

                # mover al siguiente día después del segmento
                current = segment_end + timedelta(days=1)

            # Si se crearon descuentos, vincular el primero (para compatibilidad)
            if descuentos_creados:
                permiso.descuento_id = descuentos_creados[0]

        db.session.commit()

        registrar_operacion_crud(
            current_user, 'permisos', 'UPDATE', 'permisos',
            permiso_id, {'estado': 'APROBADO', 'descuento_id': permiso.descuento_id}
        )

        flash('Permiso aprobado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al aprobar permiso: {str(e)}', 'danger')
    
    return redirect(url_for('rrhh.listar_permisos'))


@rrhh_bp.route('/permisos/<int:permiso_id>/anular', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def anular_permiso(permiso_id):
    """Anular un permiso (revertir descuento asociado si existe)."""
    permiso = Permiso.query.get_or_404(permiso_id)

    try:
        from ..models import EstadoPermisoEnum, Descuento

        permiso.estado = EstadoPermisoEnum.RECHAZADO

        # Marcar descuentos asociados inactivos (no borrarlos)
        descuentos = Descuento.query.filter_by(origen_tipo='permiso', origen_id=permiso.id, activo=True).all()
        for d in descuentos:
            d.activo = False

        if permiso.descuento_id:
            d = Descuento.query.get(permiso.descuento_id)
            if d:
                d.activo = False
            permiso.descuento_id = None

        db.session.commit()

        registrar_operacion_crud(
            current_user, 'permisos', 'UPDATE', 'permisos',
            permiso_id, {'accion': 'ANULAR', 'descuento_revertido': True}
        )

        flash('Permiso anulado y descuento revertido si existía', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al anular permiso: {str(e)}', 'danger')

    return redirect(url_for('rrhh.listar_permisos'))

@rrhh_bp.route('/permisos/<int:permiso_id>/rechazar', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def rechazar_permiso(permiso_id):
    """Rechazar permiso"""
    permiso = Permiso.query.get_or_404(permiso_id)
    
    try:
        from ..models import EstadoPermisoEnum, Descuento

        permiso.estado = EstadoPermisoEnum.RECHAZADO

        # Marcar como inactivos los descuentos asociados a este permiso (no borrarlos)
        descuentos = Descuento.query.filter_by(origen_tipo='permiso', origen_id=permiso.id, activo=True).all()
        for d in descuentos:
            d.activo = False

        # También si hay descuento_id directo, inactivarlo y limpiar el campo
        if permiso.descuento_id:
            d = Descuento.query.get(permiso.descuento_id)
            if d:
                d.activo = False
            permiso.descuento_id = None

        db.session.commit()

        registrar_operacion_crud(
            current_user, 'permisos', 'UPDATE', 'permisos',
            permiso_id, {'estado': 'RECHAZADO', 'descuento_revertido': True}
        )

        flash('Permiso rechazado', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al rechazar permiso: {str(e)}', 'danger')
    
    return redirect(url_for('rrhh.listar_permisos'))

# ==================== SANCIONES ====================
@rrhh_bp.route('/sanciones', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def listar_sanciones():
    """Lista sanciones"""
    registrar_bitacora(current_user, 'sanciones', 'VIEW', 'sanciones')
    
    pagina = request.args.get('page', 1, type=int)
    sanciones = Sancion.query.paginate(page=pagina, per_page=10)
    
    return render_template('rrhh/sanciones.html', sanciones=sanciones)

@rrhh_bp.route('/sanciones/crear', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def crear_sancion():
    """Crear sanción"""
    empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
    
    if request.method == 'POST':
        try:
            sancion = Sancion(
                empleado_id=int(request.form.get('empleado_id')),
                tipo_sancion=request.form.get('tipo_sancion'),
                motivo=request.form.get('motivo'),
                fecha=datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date(),
                monto=Decimal(request.form.get('monto', 0)),
                descripcion=request.form.get('descripcion')
            )
            
            db.session.add(sancion)
            db.session.commit()

            # Si la sanción es 'Suspensión' y se indicó días, crear descuentos automáticos
            try:
                dias_susp = int(request.form.get('dias_suspension', 0))
            except Exception:
                dias_susp = 0

            if sancion.tipo_sancion and 'suspension' in sancion.tipo_sancion.lower() and dias_susp > 0:
                from ..models import Descuento
                empleado = sancion.empleado
                salario = Decimal(empleado.salario_base)
                fecha_start = sancion.fecha
                fecha_end = fecha_start + timedelta(days=dias_susp-1)

                current = fecha_start
                while current <= fecha_end:
                    last_day = calendar.monthrange(current.year, current.month)[1]
                    end_of_month = date(current.year, current.month, last_day)
                    segment_end = end_of_month if end_of_month <= fecha_end else fecha_end

                    dias_segment = (segment_end - current).days + 1
                    monto_segment = (salario / Decimal('30')) * Decimal(dias_segment)
                    monto_segment = monto_segment.quantize(Decimal('0.01'))

                    desc = Descuento(
                        empleado_id=empleado.id,
                        tipo='Sancion - Suspensión',
                        monto=monto_segment,
                        mes=current.month,
                        año=current.year,
                        descripcion=f'Descuento por sanción id {sancion.id}',
                        activo=True,
                        origen_tipo='sancion',
                        origen_id=sancion.id
                    )
                    db.session.add(desc)
                    db.session.flush()

                    current = segment_end + timedelta(days=1)

                db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'sanciones', 'CREATE', 'sanciones',
                sancion.id, {'empleado_id': sancion.empleado_id, 'tipo': sancion.tipo_sancion}
            )
            
            flash('Sanción registrada exitosamente', 'success')
            return redirect(url_for('rrhh.listar_sanciones'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar sanción: {str(e)}', 'danger')
    
    return render_template('rrhh/crear_sancion.html', empleados=empleados)

# ==================== LIQUIDACIONES ====================
@rrhh_bp.route('/liquidaciones', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def listar_liquidaciones():
    """Lista liquidaciones"""
    registrar_bitacora(current_user, 'liquidaciones', 'VIEW', 'liquidaciones')
    
    pagina = request.args.get('page', 1, type=int)
    periodo_filtro = request.args.get('periodo', f'{date.today().strftime("%Y-%m")}')
    
    liquidaciones = Liquidacion.query.filter_by(periodo=periodo_filtro).paginate(page=pagina, per_page=10)
    
    return render_template('rrhh/liquidaciones.html', liquidaciones=liquidaciones, periodo=periodo_filtro)

@rrhh_bp.route('/liquidaciones/generar', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def generar_liquidacion():
    """Generar liquidaciones para un período"""
    if request.method == 'POST':
        try:
            periodo = request.form.get('periodo')  # YYYY-MM
            año, mes = map(int, periodo.split('-'))
            
            # Obtener todos los empleados activos
            empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
            
            contador = 0
            for empleado in empleados:
                # Evitar duplicados
                liquidacion_existente = Liquidacion.query.filter_by(
                    empleado_id=empleado.id,
                    periodo=periodo
                ).first()
                
                if liquidacion_existente:
                    continue
                
                # ========================================
                # CALCULAR DÍAS TRABAJADOS DESDE ASISTENCIAS
                # ========================================
                dias_presentes = db.session.query(func.count(Asistencia.id)).filter(
                    Asistencia.empleado_id == empleado.id,
                    func.extract('month', Asistencia.fecha) == mes,
                    func.extract('year', Asistencia.fecha) == año,
                    Asistencia.presente == True
                ).scalar() or 0
                
                # Calcular días hábiles teóricos del mes (lunes a viernes)
                import calendar
                primer_dia = date(año, mes, 1)
                ultimo_dia = date(año, mes, calendar.monthrange(año, mes)[1])
                
                dias_habiles_teoricos = 0
                fecha_actual = primer_dia
                while fecha_actual <= ultimo_dia:
                    if fecha_actual.weekday() < 5:  # Lunes a viernes
                        dias_habiles_teoricos += 1
                    fecha_actual += timedelta(days=1)
                
                dias_ausentes = dias_habiles_teoricos - dias_presentes
                
                # ========================================
                # CALCULAR SALARIO PROPORCIONAL
                # ========================================
                salario_diario = empleado.salario_base / Decimal(30)
                salario_base_ajustado = salario_diario * Decimal(str(dias_presentes))
                
                # Calcular ingresos extras
                ingresos_extras = db.session.query(func.sum(IngresoExtra.monto)).filter(
                    IngresoExtra.empleado_id == empleado.id,
                    IngresoExtra.mes == mes,
                    IngresoExtra.año == año
                ).scalar() or Decimal('0')
                
                # Calcular descuentos
                descuentos = db.session.query(func.sum(Descuento.monto)).filter(
                    Descuento.empleado_id == empleado.id,
                    Descuento.mes == mes,
                    Descuento.año == año
                ).scalar() or Decimal('0')
                
                # Calcular aporte IPS (9.625% sobre salario ajustado)
                aporte_ips = (salario_base_ajustado + ingresos_extras) * Decimal('0.09625')
                
                # Calcular salario neto
                salario_neto = salario_base_ajustado + ingresos_extras - descuentos - aporte_ips
                
                # Crear liquidación
                liquidacion = Liquidacion(
                    empleado_id=empleado.id,
                    periodo=periodo,
                    salario_base=salario_base_ajustado,  # Salario ajustado a días trabajados
                    ingresos_extras=ingresos_extras,
                    descuentos=descuentos,
                    aporte_ips=aporte_ips,
                    salario_neto=salario_neto,
                    dias_trabajados=dias_presentes
                )
                
                db.session.add(liquidacion)
                contador += 1
            
            db.session.commit()
            
            registrar_bitacora(
                current_user, 'liquidaciones', 'CREATE', 'liquidaciones',
                detalle=f'Generadas {contador} liquidaciones para período {periodo}'
            )
            
            flash(f'{contador} liquidaciones generadas exitosamente (cálculo basado en asistencias)', 'success')
            return redirect(url_for('rrhh.listar_liquidaciones', periodo=periodo))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al generar liquidaciones: {str(e)}', 'danger')
    
    return render_template('rrhh/generar_liquidacion.html')

@rrhh_bp.route('/liquidaciones/<int:liquidacion_id>/descargar-pdf', methods=['GET'])
@login_required
def descargar_recibo_pdf(liquidacion_id):
    """Descargar recibo de salario en PDF"""
    liquidacion = Liquidacion.query.get_or_404(liquidacion_id)
    empleado = liquidacion.empleado
    
    registrar_bitacora(
        current_user, 'liquidaciones', 'VIEW', 'liquidaciones',
        liquidacion_id, 'Descarga de recibo PDF'
    )
    
    # Generar PDF
    pdf_buffer = ReportUtils.generar_recibo_salario(empleado, liquidacion)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'recibo_{empleado.codigo}_{liquidacion.periodo}.pdf'
    )

@rrhh_bp.route('/liquidaciones/planilla-mensual/<periodo>/pdf', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def descargar_planilla_mensual(periodo):
    """Descargar planilla mensual consolidada"""
    liquidaciones = Liquidacion.query.filter_by(periodo=periodo).all()
    empleados_liquidaciones = [(l.empleado, l) for l in liquidaciones]
    
    if not empleados_liquidaciones:
        flash('No hay liquidaciones para ese período', 'warning')
        return redirect(url_for('rrhh.listar_liquidaciones', periodo=periodo))
    
    registrar_bitacora(
        current_user, 'liquidaciones', 'VIEW', 'liquidaciones',
        detalle=f'Descarga de planilla mensual {periodo}'
    )
    
    pdf_buffer = ReportUtils.generar_planilla_mensual(empleados_liquidaciones, periodo)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'planilla_mensual_{periodo}.pdf'
    )

# ==================== VACACIONES ====================
@rrhh_bp.route('/vacaciones', methods=['GET'])
@login_required
def listar_vacaciones():
    """Lista vacaciones"""
    registrar_bitacora(current_user, 'vacaciones', 'VIEW', 'vacaciones')
    
    pagina = request.args.get('page', 1, type=int)
    # Normalizar el filtro de año a int (request.args devuelve str si viene por querystring)
    año_filtro_raw = request.args.get('año', date.today().year)
    try:
        año_filtro = int(año_filtro_raw)
    except (TypeError, ValueError):
        año_filtro = date.today().year

    vacaciones = Vacacion.query.filter_by(año=año_filtro).paginate(page=pagina, per_page=10)
    
    return render_template('rrhh/vacaciones.html', vacaciones=vacaciones, año=año_filtro)


@rrhh_bp.route('/vacaciones/empleado/<int:empleado_id>', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def ver_historial_vacaciones(empleado_id):
    """Ver historial de vacaciones de un empleado y sus solicitudes pendientes"""
    registrar_bitacora(current_user, 'vacaciones', 'VIEW', 'vacaciones')

    empleado = Empleado.query.get_or_404(empleado_id)
    # Traer todas las vacaciones (historial) del empleado, ordenadas por año descendente
    vacaciones = Vacacion.query.filter_by(empleado_id=empleado_id).order_by(Vacacion.año.desc()).all()
    # Traer solicitudes pendientes (si las hubiera)
    pendientes = Vacacion.query.filter_by(empleado_id=empleado_id, estado=EstadoVacacionEnum.PENDIENTE).all()

    return render_template('rrhh/vacacion_detalle.html', empleado=empleado, vacaciones=vacaciones, pendientes=pendientes)


@rrhh_bp.route('/vacaciones/solicitud_imprimir', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def imprimir_solicitud_vacacion():
    """Generar PDF de solicitud de vacaciones para imprimir y firmar"""
    empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()

    if request.method == 'POST':
        try:
            empleado_id = int(request.form.get('empleado_id'))
            empleado = Empleado.query.get_or_404(empleado_id)

            # Priorizar si viene vacacion_id (imprimir solicitud existente)
            vacacion_id = request.form.get('vacacion_id')
            if vacacion_id:
                vacacion = Vacacion.query.get(int(vacacion_id))
                fecha_inicio = vacacion.fecha_inicio_solicitud
                fecha_fin = vacacion.fecha_fin_solicitud
                dias = (fecha_fin - fecha_inicio).days + 1 if fecha_inicio and fecha_fin else ''
            else:
                # Tomar datos manuales
                fecha_inicio = request.form.get('fecha_inicio') and datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date()
                fecha_fin = request.form.get('fecha_fin') and datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%d').date()
                dias = (fecha_fin - fecha_inicio).days + 1 if fecha_inicio and fecha_fin else ''

            # Generar PDF
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4

            # Encabezado
            c.setFont('Helvetica-Bold', 14)
            c.drawString(50, height - 50, 'Solicitud de Vacaciones')
            c.setFont('Helvetica', 10)
            c.drawString(50, height - 80, f'Fecha de solicitud: {datetime.now().strftime("%d/%m/%Y")}')

            # Datos del empleado
            c.setFont('Helvetica-Bold', 11)
            c.drawString(50, height - 120, 'Datos del funcionario:')
            c.setFont('Helvetica', 10)
            c.drawString(60, height - 140, f'Nombre: {empleado.nombre}')
            c.drawString(300, height - 140, f'Apellido: {empleado.apellido}')
            c.drawString(60, height - 160, f'Código: {empleado.codigo}')
            c.drawString(60, height - 180, f'Días a solicitar: {dias}')
            c.drawString(60, height - 200, f'Periodo solicitado: {fecha_inicio.strftime("%d/%m/%Y") if fecha_inicio else "-"} - {fecha_fin.strftime("%d/%m/%Y") if fecha_fin else "-"}')

            # Espacio para firmas
            y_sig = height - 260
            line_y_gap = 60
            c.line(60, y_sig, 260, y_sig)
            c.drawString(60, y_sig - 15, 'Firma del funcionario')

            c.line(300, y_sig, 500, y_sig)
            c.drawString(300, y_sig - 15, 'Firma del jefe')

            c.line(60, y_sig - line_y_gap, 260, y_sig - line_y_gap)
            c.drawString(60, y_sig - line_y_gap - 15, 'Firma RRHH')

            # Pie
            c.setFont('Helvetica-Oblique', 9)
            c.drawString(50, 40, 'Este documento es la solicitud formal del funcionario para gestionar sus vacaciones ante RRHH.')

            c.showPage()
            c.save()
            buffer.seek(0)

            filename = f'solicitud_vacaciones_{empleado.codigo}_{datetime.now().strftime("%Y%m%d")}.pdf'
            return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)

        except Exception as e:
            flash(f'Error generando PDF: {e}', 'danger')

    # GET
    return render_template('rrhh/vacacion_imprimir.html', empleados=empleados)


@rrhh_bp.route('/vacaciones/solicitud_imprimir_modelo', methods=['GET'])
@login_required
def imprimir_solicitud_vacacion_modelo():
    """Generar y descargar el PDF modelo en blanco para que el funcionario lo complete manualmente."""
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        c.setFont('Helvetica-Bold', 16)
        c.drawString(50, height - 50, 'Solicitud de Vacaciones (Modelo)')
        c.setFont('Helvetica', 10)
        c.drawString(50, height - 80, f'Fecha: {datetime.now().strftime("%d/%m/%Y")}')

        # Campos en blanco para completar
        y = height - 120
        field_gap = 24
        c.drawString(50, y, 'Nombre:')
        c.line(120, y - 3, 500, y - 3)
        y -= field_gap

        c.drawString(50, y, 'Apellido:')
        c.line(120, y - 3, 500, y - 3)
        y -= field_gap

        c.drawString(50, y, 'Código:')
        c.line(120, y - 3, 300, y - 3)
        y -= field_gap

        c.drawString(50, y, 'Días a solicitar:')
        c.line(150, y - 3, 220, y - 3)
        y -= field_gap

        c.drawString(50, y, 'Periodo solicitado (desde - hasta):')
        c.line(240, y - 3, 500, y - 3)
        y -= (field_gap + 10)

        # Espacio para firmas
        sig_y = y - 40
        c.line(60, sig_y, 260, sig_y)
        c.drawString(60, sig_y - 15, 'Firma del funcionario')

        c.line(300, sig_y, 500, sig_y)
        c.drawString(300, sig_y - 15, 'Firma del jefe')

        c.line(60, sig_y - 80, 260, sig_y - 80)
        c.drawString(60, sig_y - 95, 'Firma RRHH')

        c.setFont('Helvetica-Oblique', 9)
        c.drawString(50, 40, 'Imprimir y entregar este formulario completo a RRHH para la gestión de la solicitud.')

        c.showPage()
        c.save()
        buffer.seek(0)
        filename = f'modelo_solicitud_vacaciones_{datetime.now().strftime("%Y%m%d")}.pdf'
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'Error generando PDF modelo: {e}', 'danger')
        return redirect(url_for('rrhh.listar_vacaciones'))


@rrhh_bp.route('/vacaciones/solicitud_imprimir_directa/<int:empleado_id>', methods=['GET'])
@login_required
def imprimir_solicitud_vacacion_directa(empleado_id):
    """Generar PDF prellenado para un empleado y descargarlo directamente (opcional vacacion_id en querystring)."""
    try:
        empleado = Empleado.query.get_or_404(empleado_id)
        vacacion_id = request.args.get('vacacion_id')
        fecha_inicio = fecha_fin = None
        dias = ''
        if vacacion_id:
            vac = Vacacion.query.get(int(vacacion_id))
            if vac:
                fecha_inicio = vac.fecha_inicio_solicitud
                fecha_fin = vac.fecha_fin_solicitud
                if fecha_inicio and fecha_fin:
                    dias = (fecha_fin - fecha_inicio).days + 1

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Encabezado simple
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, height - 50, 'Solicitud de Vacaciones')
        c.setFont('Helvetica', 10)
        c.drawString(50, height - 80, f'Fecha de solicitud: {datetime.now().strftime("%d/%m/%Y")}')

        # Datos del empleado prellenados
        c.setFont('Helvetica-Bold', 11)
        c.drawString(50, height - 120, 'Datos del funcionario:')
        c.setFont('Helvetica', 10)
        c.drawString(60, height - 140, f'Nombre: {empleado.nombre}')
        c.drawString(300, height - 140, f'Apellido: {empleado.apellido}')
        c.drawString(60, height - 160, f'Código: {empleado.codigo}')
        c.drawString(60, height - 180, f'Días a solicitar: {dias}')
        c.drawString(60, height - 200, f'Periodo solicitado: {fecha_inicio.strftime("%d/%m/%Y") if fecha_inicio else "-"} - {fecha_fin.strftime("%d/%m/%Y") if fecha_fin else "-"}')

        # Espacio para firmas
        y_sig = height - 260
        c.line(60, y_sig, 260, y_sig)
        c.drawString(60, y_sig - 15, 'Firma del funcionario')

        c.line(300, y_sig, 500, y_sig)
        c.drawString(300, y_sig - 15, 'Firma del jefe')

        c.line(60, y_sig - 60, 260, y_sig - 60)
        c.drawString(60, y_sig - 75, 'Firma RRHH')

        c.setFont('Helvetica-Oblique', 9)
        c.drawString(50, 40, 'Este documento es la solicitud formal del funcionario para gestionar sus vacaciones ante RRHH.')

        c.showPage()
        c.save()
        buffer.seek(0)

        filename = f'solicitud_vacaciones_{empleado.codigo}_{datetime.now().strftime("%Y%m%d")}.pdf'
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'Error generando PDF: {e}', 'danger')
        return redirect(url_for('rrhh.listar_vacaciones'))

@rrhh_bp.route('/vacaciones/solicitar', methods=['GET', 'POST'])
@login_required
def solicitar_vacaciones():
    """Solicitar vacaciones"""
    empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
    
    if request.method == 'POST':
        try:
            empleado_id = int(request.form.get('empleado_id'))
            fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%d').date()
            dias_solicitados = (fecha_fin - fecha_inicio).days + 1
            
            # Verificar días disponibles
            vacacion = Vacacion.query.filter_by(
                empleado_id=empleado_id,
                año=fecha_inicio.year
            ).first()
            
            if not vacacion:
                vacacion = Vacacion(
                    empleado_id=empleado_id,
                    año=fecha_inicio.year,
                    dias_disponibles=15
                )
                db.session.add(vacacion)
                db.session.flush()

            # Asegurar que la solicitud quede en estado PENDIENTE y actualizar dias_pendientes
            from ..models import EstadoVacacionEnum
            vacacion.estado = EstadoVacacionEnum.PENDIENTE
            # Mantener dias_pendientes coherentes (no restamos hasta la aprobación)
            try:
                vacacion.dias_pendientes = max((vacacion.dias_disponibles - (vacacion.dias_tomados or 0)), 0)
            except Exception:
                # Seguridad: si hay valores inesperados, dejar el valor por defecto
                pass
            
            if vacacion.dias_disponibles < dias_solicitados:
                flash(f'Solo dispone de {vacacion.dias_disponibles} días de vacaciones', 'danger')
                return redirect(url_for('rrhh.solicitar_vacaciones'))
            
            vacacion.fecha_inicio_solicitud = fecha_inicio
            vacacion.fecha_fin_solicitud = fecha_fin
            
            db.session.commit()
            
            registrar_operacion_crud(
                current_user, 'vacaciones', 'CREATE', 'vacaciones',
                vacacion.id, {'empleado_id': empleado_id, 'dias': dias_solicitados}
            )
            
            flash('Solicitud de vacaciones realizada exitosamente', 'success')
            return redirect(url_for('rrhh.listar_vacaciones'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al solicitar vacaciones: {str(e)}', 'danger')
    
    return render_template('rrhh/solicitar_vacaciones.html', empleados=empleados)

@rrhh_bp.route('/vacaciones/<int:vacacion_id>/aprobar', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def aprobar_vacacion(vacacion_id):
    """Aprobar solicitud de vacaciones"""
    vacacion = Vacacion.query.get_or_404(vacacion_id)
    
    try:
        from ..models import EstadoVacacionEnum
        vacacion.estado = EstadoVacacionEnum.APROBADA
        # Actualizar días disponibles
        dias_solicitados = (vacacion.fecha_fin_solicitud - vacacion.fecha_inicio_solicitud).days + 1
        vacacion.dias_disponibles -= dias_solicitados
        vacacion.dias_tomados += dias_solicitados
        vacacion.dias_pendientes -= dias_solicitados
        db.session.commit()
        
        registrar_operacion_crud(
            current_user, 'vacaciones', 'UPDATE', 'vacaciones',
            vacacion_id, {'estado': 'APROBADA', 'dias': dias_solicitados}
        )
        
        flash(f'Vacación aprobada exitosamente ({dias_solicitados} días)', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al aprobar vacación: {str(e)}', 'danger')
    
    return redirect(url_for('rrhh.listar_vacaciones'))

@rrhh_bp.route('/vacaciones/<int:vacacion_id>/rechazar', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def rechazar_vacacion(vacacion_id):
    """Rechazar solicitud de vacaciones"""
    vacacion = Vacacion.query.get_or_404(vacacion_id)
    
    try:
        from ..models import EstadoVacacionEnum
        vacacion.estado = EstadoVacacionEnum.RECHAZADA
        db.session.commit()
        
        registrar_operacion_crud(
            current_user, 'vacaciones', 'UPDATE', 'vacaciones',
            vacacion_id, {'estado': 'RECHAZADA'}
        )
        
        flash('Solicitud de vacaciones rechazada', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al rechazar vacación: {str(e)}', 'danger')
    
    return redirect(url_for('rrhh.listar_vacaciones'))

# ==================== DESPIDOS ====================

def calcular_antiguedad_años(fecha_inicio, fecha_fin):
    """Calcula años completos entre dos fechas."""
    diferencia = fecha_fin - fecha_inicio
    años = diferencia.days // 365
    return años

def calcular_indemnizacion(salario_base, tipo_despido, antiguedad_años):
    """
    Calcula indemnización por despido.
    - Justificado: 0 (sin indemnización)
    - Injustificado: 1 mes + 1 mes por año (máx 12 meses)
    """
    if tipo_despido == 'justificado':
        return Decimal('0')
    
    # Injustificado: 1 + años (máximo 12 meses)
    meses = min(1 + antiguedad_años, 12)
    return (Decimal(meses) * Decimal(str(salario_base))).quantize(Decimal('0.01'))

def calcular_aguinaldo_proporcional(salario_base, fecha_despido):
    """
    Calcula aguinaldo proporcional (13º sueldo).
    Retorna proporción del año calendario trabajado.
    """
    año_despido = fecha_despido.year
    fecha_inicio_año = datetime(año_despido, 1, 1).date()
    
    # Días trabajados desde inicio del año (inclusive)
    días_trabajados = (fecha_despido - fecha_inicio_año).days + 1
    meses_trabajados = Decimal(str(días_trabajados)) / Decimal('30')
    
    aguinaldo = (Decimal(str(salario_base)) * meses_trabajados / Decimal('12')).quantize(Decimal('0.01'))
    return aguinaldo

def calcular_vacaciones_no_gozadas(empleado, fecha_despido):
    """
    Calcula monto de vacaciones no gozadas.
    - Suma vacaciones aprobadas no tomadas de años anteriores
    - Suma proporción de derechos en año actual (2 días por mes)
    """
    # Vacaciones registradas pero no completadas (asumimos que registros con estado 'aprobada' no gozadas están aquí)
    from ..models import EstadoVacacionEnum
    
    # Acumular vacaciones no gozadas del año anterior
    año_anterior = fecha_despido.year - 1
    vacaciones_año_ant = db.session.query(db.func.count(Vacacion.id)).filter(
        Vacacion.empleado_id == empleado.id,
        Vacacion.año == año_anterior,
        Vacacion.estado == EstadoVacacionEnum.APROBADA
    ).scalar() or 0
    
    # Vacaciones ganadas en año actual (2 días por mes trabajado)
    días_transcurridos = (fecha_despido - datetime(fecha_despido.year, 1, 1).date()).days + 1
    meses_año_actual = Decimal(str(días_transcurridos)) / Decimal('30')
    vacaciones_ganadas_año = meses_año_actual * Decimal('2')
    
    # Total de días no gozados
    total_días = Decimal(str(vacaciones_año_ant * 2)) + vacaciones_ganadas_año  # 2 días por mes
    
    # Valor por día = salario_base / 30
    salario_diario = Decimal(str(empleado.salario_base)) / Decimal('30')
    vacaciones_monto = (total_días * salario_diario).quantize(Decimal('0.01'))
    
    return vacaciones_monto

def calcular_aportes_ips_despido(monto_liquido, porcentaje_aporte=Decimal('0.09')):
    """
    Calcula aporte a IPS (9% del empleado).
    Se aplica al total de indemnización + aguinaldo + vacaciones.
    """
    return (Decimal(str(monto_liquido)) * porcentaje_aporte).quantize(Decimal('0.01'))

def generar_liquidacion_despido(empleado_id, tipo_despido, causal=None, descripcion=None):
    """
    Genera liquidación completa por despido.
    Retorna diccionario con montos calculados y objetos creados.
    """
    empleado = Empleado.query.get(empleado_id)
    if not empleado:
        return None
    
    fecha_despido = date.today()
    
    # Calcular antigüedad
    antiguedad = calcular_antiguedad_años(empleado.fecha_contratacion, fecha_despido)
    
    # 1. Indemnización
    indemnizacion = calcular_indemnizacion(empleado.salario_base, tipo_despido, antiguedad)
    
    # 2. Aguinaldo proporcional
    aguinaldo = calcular_aguinaldo_proporcional(empleado.salario_base, fecha_despido)
    
    # 3. Vacaciones no gozadas
    vacaciones = calcular_vacaciones_no_gozadas(empleado, fecha_despido)
    
    # 4. Subtotal antes de aportes
    subtotal = indemnizacion + aguinaldo + vacaciones
    
    # 5. Aportes IPS
    aportes = calcular_aportes_ips_despido(subtotal)
    
    # 6. Total líquido
    total_liquido = subtotal - aportes
    
    # Crear registro de Despido
    despido = Despido(
        empleado_id=empleado_id,
        tipo=tipo_despido,
        causal=causal,
        descripcion=descripcion,
        fecha_despido=fecha_despido,
        usuario_id=current_user.id if current_user else None
    )
    db.session.add(despido)
    db.session.flush()
    
    # Crear registro de Liquidación
    liquidacion = Liquidacion(
        empleado_id=empleado_id,
        periodo=f"{fecha_despido.year}-{fecha_despido.month:02d}",
        salario_base=empleado.salario_base,
        salario_neto=total_liquido,
        despido_id=despido.id,
        indemnizacion_monto=indemnizacion,
        aguinaldo_monto=aguinaldo,
        vacaciones_monto=vacaciones,
        aportes_ips_despido=aportes
    )
    db.session.add(liquidacion)
    despido.liquidaciones.append(liquidacion)  # Relación inversa
    
    db.session.commit()
    
    # Registrar en bitácora
    registrar_bitacora(
        current_user,
        'despidos',
        'CREATE',
        'despidos',
        despido.id,
        f"Despido {tipo_despido}. Antigüedad: {antiguedad} años. Indemnización: {indemnizacion}"
    )
    
    return {
        'indemnizacion': indemnizacion,
        'aguinaldo': aguinaldo,
        'vacaciones': vacaciones,
        'aportes_ips': aportes,
        'total_liquido': total_liquido,
        'subtotal': subtotal,
        'antiguedad': antiguedad,
        'liquidacion_obj': liquidacion,
        'despido_obj': despido
    }

@rrhh_bp.route('/registrar_despido', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def registrar_despido():
    """Formulario y procesamiento de despido."""
    if request.method == 'POST':
        empleado_id = request.form.get('empleado_id', type=int)
        tipo = request.form.get('tipo')
        causal = request.form.get('causal', default=None)
        descripcion = request.form.get('descripcion', default=None)
        
        resultado = generar_liquidacion_despido(empleado_id, tipo, causal, descripcion)
        
        if resultado:
            flash('Despido registrado. Liquidación generada.', 'success')
            return redirect(url_for('rrhh.ver_liquidacion_despido', liquidacion_id=resultado['liquidacion_obj'].id))
        else:
            flash('Error al registrar despido.', 'danger')
    
    empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
    causales_justificadas = [
        ('incapacidad', 'Incapacidad Laboral Permanente'),
        ('ineptitud', 'Ineptitud Técnica o Manifiesta'),
        ('falta_grave', 'Falta Grave / Conducta Inapropiada'),
        ('perdida_habilitacion', 'Pérdida de Habilitación Profesional'),
        ('fuerza_mayor', 'Fuerza Mayor o Caso Fortuito'),
    ]
    
    return render_template(
        'rrhh/registrar_despido.html',
        empleados=empleados,
        causales=causales_justificadas
    )

@rrhh_bp.route('/liquidacion_despido/<int:liquidacion_id>')
@login_required
@role_required(RoleEnum.RRHH)
def ver_liquidacion_despido(liquidacion_id):
    """Vista de detalles de liquidación por despido."""
    liquidacion = Liquidacion.query.get_or_404(liquidacion_id)
    if not liquidacion.despido_id:
        flash('Esta liquidación no es de despido.', 'warning')
        return redirect(url_for('rrhh.liquidaciones'))
    
    despido = liquidacion.despido
    empleado = liquidacion.empleado
    antiguedad = calcular_antiguedad_años(empleado.fecha_contratacion, despido.fecha_despido)
    
    return render_template(
        'rrhh/liquidacion_despido.html',
        liquidacion=liquidacion,
        despido=despido,
        empleado=empleado,
        antiguedad=antiguedad
    )

@rrhh_bp.route('/liquidacion_despido/<int:liquidacion_id>/descargar_pdf')
@login_required
@role_required(RoleEnum.RRHH)
def descargar_pdf_liquidacion_despido(liquidacion_id):
    """Descarga PDF de liquidación por despido."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    
    liquidacion = Liquidacion.query.get_or_404(liquidacion_id)
    despido = liquidacion.despido
    empleado = liquidacion.empleado
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = styles['Title']
    title_style.alignment = 1  # Center
    elements.append(Paragraph("LIQUIDACIÓN POR DESPIDO", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Subtítulo
    elements.append(Paragraph(f"<b>Fecha:</b> {despido.fecha_despido.strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Datos empleado
    data = [
        ['EMPLEADO:', empleado.nombre],
        ['CÉDULA:', empleado.cedula],
        ['CARGO:', empleado.cargo.nombre if empleado.cargo else '---'],
        ['ANTIGÜEDAD:', f"{calcular_antiguedad_años(empleado.fecha_contratacion, despido.fecha_despido)} años"],
        ['TIPO DESPIDO:', despido.tipo.upper()],
        ['CAUSAL:', despido.causal.upper() if despido.causal else '---'],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f4f8')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabla de rubros
    rubros = [
        ['RUBRO', 'MONTO'],
        ['Indemnización por antigüedad', f"${float(liquidacion.indemnizacion_monto):,.2f}"],
        ['Aguinaldo (13º Sueldo) proporcional', f"${float(liquidacion.aguinaldo_monto):,.2f}"],
        ['Vacaciones no gozadas', f"${float(liquidacion.vacaciones_monto):,.2f}"],
        ['Subtotal', f"${float(liquidacion.indemnizacion_monto + liquidacion.aguinaldo_monto + liquidacion.vacaciones_monto):,.2f}"],
        ['(-) Aporte IPS (9%)', f"-${float(liquidacion.aportes_ips_despido):,.2f}"],
        ['TOTAL NETO A PAGAR', f"${float(liquidacion.salario_neto):,.2f}"],
    ]
    
    tabla_rubros = Table(rubros, colWidths=[3.5*inch, 2*inch])
    tabla_rubros.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -2), 'Helvetica', 9),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor('#D9E1F2')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(tabla_rubros)
    elements.append(Spacer(1, 0.3*inch))
    
    # Observaciones
    if despido.descripcion:
        elements.append(Paragraph("<b>Observaciones:</b>", styles['Normal']))
        elements.append(Paragraph(despido.descripcion, styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Liquidacion_Despido_{empleado.nombre.replace(' ', '_')}_{despido.fecha_despido.strftime('%Y%m%d')}.pdf"
    )

# ==================== BITACORA ====================
@rrhh_bp.route('/bitacora', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def ver_bitacora():
    """Ver bitácora de acciones"""
    from ..models import Usuario
    
    pagina = request.args.get('page', 1, type=int)
    usuario_filtro = request.args.get('usuario', '')
    modulo_filtro = request.args.get('modulo', '')
    
    query = Bitacora.query
    
    if usuario_filtro:
        query = query.filter(Bitacora.usuario.has(Usuario.nombre_usuario.ilike(f'%{usuario_filtro}%')))
    
    if modulo_filtro:
        query = query.filter(Bitacora.modulo == modulo_filtro)
    
    bitacoras = query.order_by(desc(Bitacora.fecha_creacion)).paginate(page=pagina, per_page=20)
    
    return render_template('rrhh/bitacora.html', bitacoras=bitacoras)

# ==================== AGUINALDOS ====================

def generar_aguinaldos_anual(año, mes_corte=None, día_corte=None):
    """
    Genera aguinaldos anuales para todos los empleados activos.
    
    Args:
        año: Año para el cual se calcula el aguinaldo (ej: 2025)
        mes_corte: Mes de pago (por defecto 12 - diciembre)
        día_corte: Día de pago (por defecto 31)
    
    Returns:
        Diccionario con resumen de generación
    """
    if mes_corte is None:
        mes_corte = 12
    if día_corte is None:
        día_corte = 31
    
    # Fecha de corte para cálculo
    fecha_corte = date(año, mes_corte, día_corte)
    
    # Obtener empleados activos
    empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
    
    generados = 0
    duplicados = 0
    errores = 0
    total_bruto = Decimal('0')
    total_neto = Decimal('0')
    
    for empleado in empleados:
        try:
            # Verificar si ya existe aguinaldo para este año
            liquidacion_existente = Liquidacion.query.filter(
                Liquidacion.empleado_id == empleado.id,
                Liquidacion.periodo.like(f'{año}%'),
                Liquidacion.aguinaldo_monto > 0  # Solo si ya hay aguinaldo
            ).first()
            
            if liquidacion_existente:
                duplicados += 1
                continue
            
            # Calcular aguinaldo proporcional para el año
            fecha_inicio_año = date(año, 1, 1)
            
            # Si el empleado fue contratado después del inicio del año, usar fecha de contratación
            fecha_desde = max(fecha_inicio_año, empleado.fecha_contratacion)
            
            # Si el empleado se retiró antes del corte, usar fecha de retiro
            fecha_hasta = fecha_corte
            if empleado.fecha_retiro and empleado.fecha_retiro < fecha_corte:
                fecha_hasta = empleado.fecha_retiro
            
            # Calcular días trabajados en el año
            días_trabajados = (fecha_hasta - fecha_desde).days + 1
            if días_trabajados <= 0:
                continue
            
            meses_trabajados = Decimal(str(días_trabajados)) / Decimal('30')
            
            # Aguinaldo bruto = (meses_trabajados / 12) × salario_base
            aguinaldo_bruto = (Decimal(str(empleado.salario_base)) * meses_trabajados / Decimal('12')).quantize(Decimal('0.01'))
            
            # Aportes IPS = 9% sobre aguinaldo
            aportes_ips = (aguinaldo_bruto * Decimal('0.09')).quantize(Decimal('0.01'))
            
            # Aguinaldo neto
            aguinaldo_neto = (aguinaldo_bruto - aportes_ips).quantize(Decimal('0.01'))
            
            # Crear liquidación de aguinaldo
            periodo_aguinaldo = f"{año}-{mes_corte:02d}"
            
            liquidacion = Liquidacion(
                empleado_id=empleado.id,
                periodo=periodo_aguinaldo,
                salario_base=empleado.salario_base,
                salario_neto=aguinaldo_neto,
                aguinaldo_monto=aguinaldo_bruto,
                aportes_ips_despido=aportes_ips,
                indemnizacion_monto=Decimal('0'),
                vacaciones_monto=Decimal('0'),
                ingresos_extras=Decimal('0'),
                descuentos=Decimal('0'),
                aporte_ips=Decimal('0'),
                dias_trabajados=días_trabajados
            )
            
            db.session.add(liquidacion)
            db.session.flush()
            
            generados += 1
            total_bruto += aguinaldo_bruto
            total_neto += aguinaldo_neto
            
        except Exception as e:
            errores += 1
            db.session.rollback()
            continue
    
    try:
        db.session.commit()
        registrar_bitacora(
            current_user,
            'aguinaldos',
            'CREATE',
            'liquidaciones',
            detalle=f'Aguinaldos {año} generados: {generados} empleados. Total bruto: {total_bruto}. Total neto: {total_neto}'
        )
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'error': str(e),
            'generados': 0
        }
    
    return {
        'success': True,
        'generados': generados,
        'duplicados': duplicados,
        'errores': errores,
        'total_bruto': total_bruto,
        'total_neto': total_neto,
        'fecha_corte': fecha_corte.strftime('%d/%m/%Y')
    }

@rrhh_bp.route('/aguinaldos', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def listar_aguinaldos():
    """Lista aguinaldos generados por año"""
    registrar_bitacora(current_user, 'aguinaldos', 'VIEW', 'liquidaciones')
    
    año_filtro = request.args.get('año', date.today().year, type=int)
    pagina = request.args.get('page', 1, type=int)
    
    # Obtener liquidaciones que contengan aguinaldo (aguinaldo_monto > 0)
    aguinaldos = Liquidacion.query.filter(
        Liquidacion.aguinaldo_monto > 0,
        Liquidacion.periodo.like(f'{año_filtro}%')
    ).order_by(desc(Liquidacion.fecha_generacion)).paginate(page=pagina, per_page=15)
    
    # Calcular totales para el año
    totales = db.session.query(
        func.sum(Liquidacion.aguinaldo_monto).label('total_bruto'),
        func.sum(Liquidacion.aportes_ips_despido).label('total_ips'),
        func.sum(Liquidacion.salario_neto).label('total_neto'),
        func.count(Liquidacion.id).label('cantidad')
    ).filter(
        Liquidacion.aguinaldo_monto > 0,
        Liquidacion.periodo.like(f'{año_filtro}%')
    ).first()
    
    return render_template(
        'rrhh/aguinaldos_listado.html',
        aguinaldos=aguinaldos,
        año=año_filtro,
        totales=totales or {
            'total_bruto': Decimal('0'),
            'total_ips': Decimal('0'),
            'total_neto': Decimal('0'),
            'cantidad': 0
        }
    )

@rrhh_bp.route('/generar_aguinaldos', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def generar_aguinaldos():
    """Formulario y procesamiento para generar aguinaldos anuales"""
    resultado = None
    
    if request.method == 'POST':
        año = int(request.form.get('año', date.today().year))
        mes_corte = int(request.form.get('mes_corte', 12))
        día_corte = int(request.form.get('día_corte', 31))
        acción = request.form.get('acción', 'preview')
        
        # Contar empleados activos que recibirían aguinaldo
        empleados_activos = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).count()
        
        if acción == 'preview':
            # Solo mostrar preview (preview en el mismo formulario)
            fecha_corte = date(año, mes_corte, día_corte)
            preview_datos = []
            
            empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
            
            for empleado in empleados:
                fecha_desde = max(date(año, 1, 1), empleado.fecha_contratacion)
                fecha_hasta = fecha_corte
                if empleado.fecha_retiro and empleado.fecha_retiro < fecha_corte:
                    fecha_hasta = empleado.fecha_retiro
                
                días = (fecha_hasta - fecha_desde).days + 1
                meses = Decimal(str(días)) / Decimal('30')
                
                aguinaldo = (Decimal(str(empleado.salario_base)) * meses / Decimal('12')).quantize(Decimal('0.01'))
                ips = (aguinaldo * Decimal('0.09')).quantize(Decimal('0.01'))
                neto = (aguinaldo - ips).quantize(Decimal('0.01'))
                
                preview_datos.append({
                    'empleado': empleado,
                    'meses': meses,
                    'aguinaldo_bruto': aguinaldo,
                    'ips': ips,
                    'aguinaldo_neto': neto
                })
            
            resultado = {
                'tipo': 'preview',
                'año': año,
                'fecha_corte': fecha_corte.strftime('%d/%m/%Y'),
                'datos': preview_datos,
                'total_bruto': sum(d['aguinaldo_bruto'] for d in preview_datos),
                'total_ips': sum(d['ips'] for d in preview_datos),
                'total_neto': sum(d['aguinaldo_neto'] for d in preview_datos),
                'cantidad': len(preview_datos)
            }
        
        elif acción == 'generar':
            # Generar aguinaldos reales
            resultado = generar_aguinaldos_anual(año, mes_corte, día_corte)
            resultado['tipo'] = 'generado'
            
            if resultado['success']:
                flash(
                    f"✓ {resultado['generados']} aguinaldos generados. Total: {resultado['total_neto']:,.2f} Gs.",
                    'success'
                )
                return redirect(url_for('rrhh.listar_aguinaldos', año=año))
            else:
                flash(f"Error al generar aguinaldos: {resultado.get('error', 'Error desconocido')}", 'danger')
    
    años_disponibles = list(range(date.today().year, 2020, -1))
    
    return render_template(
        'rrhh/generar_aguinaldos.html',
        resultado=resultado,
        años_disponibles=años_disponibles,
        año_actual=date.today().year
    )

# ==================== LEGAJO DIGITAL / PERFIL EMPLEADO ====================

@rrhh_bp.route('/empleados/<int:empleado_id>/perfil', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def perfil_empleado(empleado_id):
    """Muestra el perfil/legajo completo del empleado"""
    empleado = Empleado.query.get_or_404(empleado_id)
    registrar_bitacora(current_user, 'empleados', 'VIEW', 'empleados', empleado_id, 'ver_perfil')
    
    return render_template('rrhh/empleado_perfil.html', empleado=empleado)

@rrhh_bp.route('/api/empleados/<int:empleado_id>/general', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def api_empleado_general(empleado_id):
    """API: Datos generales y KPIs del empleado"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    # Calcular datos
    vacaciones_total = db.session.query(func.sum(Vacacion.dias_disponibles)).filter_by(empleado_id=empleado_id).scalar() or 0
    vacaciones_tomadas = db.session.query(func.sum(Vacacion.dias_tomados)).filter_by(empleado_id=empleado_id).scalar() or 0
    vacaciones_pendientes = vacaciones_total - vacaciones_tomadas
    
    sanciones_activas = Sancion.query.filter_by(empleado_id=empleado_id).count()
    
    # Permisos usados: contar los que fueron aprobados o completados
    permisos_usados = Permiso.query.filter(
        Permiso.empleado_id == empleado_id,
        or_(Permiso.estado == EstadoPermisoEnum.APROBADO, Permiso.estado == EstadoPermisoEnum.COMPLETADO)
    ).count()
    
    # Asistencia del mes actual
    mes_actual = date.today().month
    año_actual = date.today().year
    asistencias_mes = db.session.query(func.count(Asistencia.id)).filter(
        Asistencia.empleado_id == empleado_id,
        func.extract('month', Asistencia.fecha) == mes_actual,
        func.extract('year', Asistencia.fecha) == año_actual,
        Asistencia.presente == True
    ).scalar() or 0
    
    dias_habiles_mes = len([d for d in calendar.monthcalendar(año_actual, mes_actual) 
                           for dow in d if dow != 0 and datetime(año_actual, mes_actual, dow).weekday() < 5])
    
    porcentaje_asistencia = (asistencias_mes / dias_habiles_mes * 100) if dias_habiles_mes > 0 else 0
    
    # Resumen de asistencia de hoy
    resumen_hoy = _resumir_dia_asistencias(empleado_id, date.today())

    return jsonify({
        'id': empleado.id,
        'codigo': empleado.codigo,
        'nombre_completo': empleado.nombre_completo,
        'cargo': empleado.cargo.nombre,
        'email': empleado.email,
        'telefono': empleado.telefono,
        'fecha_ingreso': empleado.fecha_ingreso.strftime('%d/%m/%Y') if empleado.fecha_ingreso else 'N/A',
        'antiguedad': empleado.antiguedad_texto,
        'estado': empleado.estado.value,
        'salario_base': float(empleado.salario_base),
        'vacaciones_pendientes': int(vacaciones_pendientes),
        'vacaciones_total': int(vacaciones_total),
        'sanciones_activas': sanciones_activas,
        'permisos_usados': permisos_usados,
        'asistencia_mes': f"{porcentaje_asistencia:.1f}%",
        'asistencias_count': asistencias_mes,
        'resumen_hoy': resumen_hoy
    })

@rrhh_bp.route('/api/empleados/<int:empleado_id>/asistencias', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def api_empleado_asistencias(empleado_id):
    """API: Asistencias del empleado con paginación y filtros"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    mes = request.args.get('mes', type=int)
    año = request.args.get('year', type=int)
    pagina = request.args.get('page', 1, type=int)
    por_pagina = request.args.get('per_page', 20, type=int)
    
    query = Asistencia.query.filter_by(empleado_id=empleado_id).order_by(desc(Asistencia.fecha))
    
    if mes and año:
        query = query.filter(
            func.extract('month', Asistencia.fecha) == mes,
            func.extract('year', Asistencia.fecha) == año
        )
    
    paginated = query.paginate(page=pagina, per_page=por_pagina)
    
    asistencias = [{
        'id': a.id,
        'fecha': a.fecha.strftime('%d/%m/%Y'),
        'entrada': a.hora_entrada.strftime('%H:%M') if a.hora_entrada else '-',
        'salida': a.hora_salida.strftime('%H:%M') if a.hora_salida else '-',
        'presente': 'Sí' if a.presente else 'No',
        'observaciones': a.observaciones or '-'
    } for a in paginated.items]
    
    return jsonify({
        'items': asistencias,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': pagina,
        'per_page': por_pagina
    })

@rrhh_bp.route('/api/empleados/<int:empleado_id>/vacaciones', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def api_empleado_vacaciones(empleado_id):
    """API: Histórico de vacaciones"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    vacaciones = Vacacion.query.filter_by(empleado_id=empleado_id).order_by(desc(Vacacion.año)).all()
    
    datos = [{
        'año': v.año,
        'dias_disponibles': v.dias_disponibles,
        'dias_tomados': v.dias_tomados,
        'dias_pendientes': v.dias_pendientes,
        'fecha_inicio': v.fecha_inicio_solicitud.strftime('%d/%m/%Y') if v.fecha_inicio_solicitud else '-',
        'fecha_fin': v.fecha_fin_solicitud.strftime('%d/%m/%Y') if v.fecha_fin_solicitud else '-',
        'estado': v.estado.value if v.estado else 'N/A'
    } for v in vacaciones]
    
    return jsonify({
        'items': datos,
        'total': len(datos)
    })

@rrhh_bp.route('/api/empleados/<int:empleado_id>/permisos', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def api_empleado_permisos(empleado_id):
    """API: Permisos del empleado con paginación"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    pagina = request.args.get('page', 1, type=int)
    por_pagina = request.args.get('per_page', 15, type=int)
    
    query = Permiso.query.filter_by(empleado_id=empleado_id).order_by(desc(Permiso.fecha_inicio))
    paginated = query.paginate(page=pagina, per_page=por_pagina)
    
    permisos = [{
        'id': p.id,
        'tipo': p.tipo_permiso,
        'motivo': p.motivo,
        'fecha_inicio': p.fecha_inicio.strftime('%d/%m/%Y'),
        'fecha_fin': p.fecha_fin.strftime('%d/%m/%Y'),
        'dias': p.dias_solicitados or ((p.fecha_fin - p.fecha_inicio).days + 1),
        'estado': p.estado.value if p.estado else 'N/A',
        'con_goce': 'Sí' if p.con_goce else 'No',
        'justificativo': p.justificativo_archivo if getattr(p, 'justificativo_archivo', None) else None
    } for p in paginated.items]
    
    return jsonify({
        'items': permisos,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': pagina,
        'per_page': por_pagina
    })

@rrhh_bp.route('/api/empleados/<int:empleado_id>/sanciones', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def api_empleado_sanciones(empleado_id):
    """API: Sanciones del empleado con paginación"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    pagina = request.args.get('page', 1, type=int)
    por_pagina = request.args.get('per_page', 15, type=int)
    
    query = Sancion.query.filter_by(empleado_id=empleado_id).order_by(desc(Sancion.fecha))
    paginated = query.paginate(page=pagina, per_page=por_pagina)
    
    sanciones = [{
        'id': s.id,
        'tipo': s.tipo_sancion,
        'motivo': s.motivo,
        'monto': float(s.monto),
        'fecha': s.fecha.strftime('%d/%m/%Y'),
        'descripcion': s.descripcion or '-',
        'justificativo': s.justificativo_archivo if getattr(s, 'justificativo_archivo', None) else None
    } for s in paginated.items]
    
    return jsonify({
        'items': sanciones,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': pagina,
        'per_page': por_pagina
    })

@rrhh_bp.route('/api/empleados/<int:empleado_id>/liquidaciones', methods=['GET'])
@login_required
@role_required(RoleEnum.RRHH)
def api_empleado_liquidaciones(empleado_id):
    """API: Histórico de liquidaciones con paginación"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    pagina = request.args.get('page', 1, type=int)
    por_pagina = request.args.get('per_page', 12, type=int)
    
    query = Liquidacion.query.filter_by(empleado_id=empleado_id).order_by(desc(Liquidacion.periodo))
    paginated = query.paginate(page=pagina, per_page=por_pagina)
    
    liquidaciones = [{
        'id': l.id,
        'periodo': l.periodo,
        'salario_base': float(l.salario_base),
        'ingresos_extras': float(l.ingresos_extras),
        'descuentos': float(l.descuentos),
        'aporte_ips': float(l.aporte_ips),
        'salario_neto': float(l.salario_neto),
        'dias_trabajados': l.dias_trabajados or 30
    } for l in paginated.items]
    
    return jsonify({
        'items': liquidaciones,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': pagina,
        'per_page': por_pagina
    })


# ===================== UPLOADS: Permisos y Sanciones =====================
@rrhh_bp.route('/permisos/<int:permiso_id>/upload-justificativo', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def upload_permiso_justificativo(permiso_id):
    """Recibe un multipart/form-data con campo 'file' y lo asocia al permiso"""
    permiso = Permiso.query.get_or_404(permiso_id)

    # aceptar 'file' o 'justificativo' como nombre de campo para compatibilidad
    if 'file' in request.files:
        file = request.files['file']
    elif 'justificativo' in request.files:
        file = request.files['justificativo']
    else:
        return jsonify({'error': 'No se recibió ningún archivo (campo "file" o "justificativo" esperado)'}), 400

    if not file or file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    filename_clean = secure_filename(file.filename)
    if not allowed_file(filename_clean):
        return jsonify({'error': 'Extensión de archivo no permitida'}), 400

    os.makedirs(PERMISOS_UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(f"perm_{permiso_id}_{int(datetime.utcnow().timestamp())}_{filename_clean}")
    filepath = os.path.join(PERMISOS_UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Guardar ruta relativa desde la carpeta 'app'
    permiso.justificativo_archivo = os.path.relpath(filepath, os.path.dirname(os.path.dirname(__file__)))
    db.session.commit()

    registrar_operacion_crud(current_user, 'permisos', 'UPDATE', 'permisos', permiso.id, {'justificativo': permiso.justificativo_archivo})

    return jsonify({'message': 'uploaded', 'ruta': permiso.justificativo_archivo}), 200


@rrhh_bp.route('/sanciones/<int:sancion_id>/upload-justificativo', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def upload_sancion_justificativo(sancion_id):
    """Recibe un multipart/form-data con campo 'file' y lo asocia a la sancion"""
    sancion = Sancion.query.get_or_404(sancion_id)

    # aceptar 'file' o 'justificativo' como nombre de campo para compatibilidad
    if 'file' in request.files:
        file = request.files['file']
    elif 'justificativo' in request.files:
        file = request.files['justificativo']
    else:
        return jsonify({'error': 'No se recibió ningún archivo (campo "file" o "justificativo" esperado)'}), 400

    if not file or file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    filename_clean = secure_filename(file.filename)
    if not allowed_file(filename_clean):
        return jsonify({'error': 'Extensión de archivo no permitida'}), 400

    os.makedirs(SANCIONES_UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(f"sanc_{sancion_id}_{int(datetime.utcnow().timestamp())}_{filename_clean}")
    filepath = os.path.join(SANCIONES_UPLOAD_FOLDER, filename)
    file.save(filepath)

    sancion.justificativo_archivo = os.path.relpath(filepath, os.path.dirname(os.path.dirname(__file__)))
    db.session.commit()

    registrar_operacion_crud(current_user, 'sanciones', 'UPDATE', 'sanciones', sancion.id, {'justificativo': sancion.justificativo_archivo})

    return jsonify({'message': 'uploaded', 'ruta': sancion.justificativo_archivo}), 200


# ===================== MÓDULO POSTULANTES (RECLUTAMIENTO) =====================

@rrhh_bp.route('/postulantes')
@login_required
@role_required(RoleEnum.RRHH)
def postulantes_lista():
    """Listado de postulantes con búsqueda y filtros"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    estado = request.args.get('estado', '', type=str)
    
    query = Postulante.query
    
    if search:
        query = query.filter(
            or_(
                Postulante.nombre.ilike(f'%{search}%'),
                Postulante.apellido.ilike(f'%{search}%'),
                Postulante.email.ilike(f'%{search}%'),
                Postulante.cargo_postulado.ilike(f'%{search}%')
            )
        )
    
    if estado:
        query = query.filter_by(estado=estado)
    
    postulantes = query.order_by(desc(Postulante.fecha_postulacion)).paginate(page=page, per_page=15)
    
    return render_template('rrhh/postulantes_lista.html', postulantes=postulantes, search=search, estado=estado)


@rrhh_bp.route('/postulantes/nuevo', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def postulante_nuevo():
    """Crear un nuevo postulante"""
    if request.method == 'POST':
        # Validar datos básicos
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        fecha_nacimiento_str = request.form.get('fecha_nacimiento', '')
        nivel_academico = request.form.get('nivel_academico', '').strip()
        cargo_postulado = request.form.get('cargo_postulado', '').strip()
        experiencia_años = request.form.get('experiencia_años', 0, type=int)
        salario_esperado = request.form.get('salario_esperado', None, type=float)
        observaciones = request.form.get('observaciones', '').strip()
        
        if not nombre or not apellido or not email or not cargo_postulado:
            flash('Nombre, apellido, email y cargo postulado son obligatorios', 'danger')
            return redirect(url_for('rrhh.postulante_nuevo'))
        
        # Verificar email único
        if Postulante.query.filter_by(email=email).first():
            flash('Este email ya está registrado como postulante', 'danger')
            return redirect(url_for('rrhh.postulante_nuevo'))
        
        # Crear postulante
        try:
            fecha_nacimiento = None
            if fecha_nacimiento_str:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
            
            postulante = Postulante(
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                nivel_academico=nivel_academico,
                cargo_postulado=cargo_postulado,
                experiencia_años=experiencia_años,
                salario_esperado=Decimal(str(salario_esperado)) if salario_esperado else None,
                estado='Nuevo',
                observaciones=observaciones,
                fecha_postulacion=date.today()
            )
            db.session.add(postulante)
            db.session.flush()  # Para obtener el ID antes de commit
            
            # Procesar archivos (CV, certificados, etc.)
            if 'documentos' in request.files:
                files = request.files.getlist('documentos')
                for file in files:
                    if file and file.filename != '':
                        if not allowed_file(file.filename):
                            flash(f'Archivo {file.filename} no permitido (solo PNG, JPG, PDF)', 'warning')
                            continue
                        
                        os.makedirs(POSTULANTES_UPLOAD_FOLDER, exist_ok=True)
                        filename_clean = secure_filename(file.filename)
                        filename = secure_filename(f"post_{postulante.id}_{int(datetime.utcnow().timestamp())}_{filename_clean}")
                        filepath = os.path.join(POSTULANTES_UPLOAD_FOLDER, filename)
                        file.save(filepath)
                        
                        # Determinar tipo de documento
                        ext = filename_clean.rsplit('.', 1)[1].lower()
                        tipo = 'CV' if filename_clean.lower().startswith('cv') else 'Certificado'
                        
                        doc = DocumentosCurriculum(
                            postulante_id=postulante.id,
                            tipo=tipo,
                            nombre_archivo=filename_clean,
                            ruta_archivo=os.path.relpath(filepath, os.path.dirname(os.path.dirname(__file__))),
                            tamaño_bytes=len(file.read()),
                            mime_type=file.content_type or 'application/octet-stream'
                        )
                        file.seek(0)  # Reset file pointer
                        tamaño_bytes = len(file.read())
                        doc.tamaño_bytes = tamaño_bytes
                        db.session.add(doc)
            
            db.session.commit()
            registrar_operacion_crud(current_user, 'postulantes', 'CREATE', 'postulantes', postulante.id, {'nombre': nombre, 'apellido': apellido, 'email': email})
            
            flash(f'Postulante {nombre} {apellido} creado exitosamente', 'success')
            return redirect(url_for('rrhh.postulante_detalle', postulante_id=postulante.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear postulante: {str(e)}', 'danger')
            return redirect(url_for('rrhh.postulante_nuevo'))
    
    return render_template('rrhh/postulante_form.html')


@rrhh_bp.route('/postulantes/<int:postulante_id>')
@login_required
@role_required(RoleEnum.RRHH)
def postulante_detalle(postulante_id):
    """Detalle de un postulante"""
    postulante = Postulante.query.get_or_404(postulante_id)
    return render_template('rrhh/postulante_detalle.html', postulante=postulante)


@rrhh_bp.route('/postulantes/<int:postulante_id>/cambiar-estado', methods=['POST'])
@login_required
@role_required(RoleEnum.RRHH)
def postulante_cambiar_estado(postulante_id):
    """Cambiar estado del postulante"""
    postulante = Postulante.query.get_or_404(postulante_id)
    nuevo_estado = request.form.get('estado', '').strip()
    
    estados_validos = ['Nuevo', 'En Evaluación', 'Contratado', 'Rechazado', 'En Espera']
    if nuevo_estado not in estados_validos:
        flash('Estado inválido', 'danger')
        return redirect(url_for('rrhh.postulante_detalle', postulante_id=postulante_id))
    
    postulante.estado = nuevo_estado
    postulante.fecha_actualizado = datetime.utcnow()
    db.session.commit()
    
    registrar_operacion_crud(current_user, 'postulantes', 'UPDATE', 'postulantes', postulante.id, {'estado': nuevo_estado})
    flash(f'Estado del postulante actualizado a: {nuevo_estado}', 'success')
    
    return redirect(url_for('rrhh.postulante_detalle', postulante_id=postulante_id))


@rrhh_bp.route('/postulantes/<int:postulante_id>/descargar-documento/<int:doc_id>')
@login_required
@role_required(RoleEnum.RRHH)
def descargar_documento_postulante(postulante_id, doc_id):
    """Descargar documento de curriculum"""
    postulante = Postulante.query.get_or_404(postulante_id)
    doc = DocumentosCurriculum.query.get_or_404(doc_id)
    
    if doc.postulante_id != postulante_id:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('rrhh.postulantes_lista'))
    
    try:
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), doc.ruta_archivo)
        return send_file(filepath, as_attachment=True, download_name=doc.nombre_archivo)
    except Exception as e:
        flash(f'Error al descargar archivo: {str(e)}', 'danger')
        return redirect(url_for('rrhh.postulante_detalle', postulante_id=postulante_id))


# ----------------- CONTRATOS (GENERACIÓN con ReportLab y almacenamiento en DB) -----------------


def _generar_numero_contrato(empleado_id):
    """Genera un número de contrato único: CONT-YYYY-EMPID-TIMESTAMP"""
    ts = int(datetime.utcnow().timestamp())
    year = datetime.utcnow().year
    return f'CONT-{year}-{empleado_id}-{ts}'


def generar_pdf_contrato(datos: dict) -> bytes:
    """Genera un PDF de contrato usando ReportLab y devuelve bytes.

    datos: dict con claves: contratante, contratado, ci, direccion_contratante, direccion_contratado,
    objeto, fecha_inicio (date), fecha_fin (date), monto, ciudad, dia, mes, ano
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Margenes
    margin_left = 50
    y = height - 70

    c.setFont('Helvetica-Bold', 14)
    c.drawString(margin_left, y, 'CONTRATO DE PRESTACIÓN DE SERVICIOS')
    y -= 30

    c.setFont('Helvetica', 11)

    # Plantilla (lineas, usando el texto provisto por el usuario)
    plantilla = (
        "Entre {contratante}, con domicilio en {direccion_contratante}, en adelante “EL CONTRATANTE”,"
        " y {contratado}, con cédula de identidad Nº {ci}, con domicilio en {direccion_contratado},"
        " en adelante “EL CONTRATADO”, se celebra el presente contrato conforme a las siguientes cláusulas:\n\n"
        "PRIMERA – Objeto\n\n"
        "EL CONTRATADO se compromete a prestar servicios de {objeto} a favor de EL CONTRATANTE.\n\n"
        "SEGUNDA – Plazo\n\n"
        "El presente contrato tendrá una duración de {meses} meses, iniciando el {fecha_inicio} y finalizando el {fecha_fin}, pudiendo renovarse por acuerdo entre las partes.\n\n"
        "TERCERA – Honorarios\n\n"
        "EL CONTRATANTE abonará a EL CONTRATADO la suma de {monto}, pagadera en {periodicidad}.\n\n"
        "CUARTA – Obligaciones\n\n"
        "EL CONTRATADO se obliga a cumplir con las tareas asignadas con responsabilidad, confidencialidad y dentro de los plazos establecidos.\n"
        "EL CONTRATANTE se compromete a proporcionar los medios y la información necesarios para la correcta ejecución del servicio.\n\n"
        "QUINTA – Terminación\n\n"
        "Cualquiera de las partes podrá rescindir el presente contrato con un preaviso de {preaviso} días, sin derecho a indemnización, salvo los honorarios devengados hasta la fecha.\n\n"
        "SEXTA – Jurisdicción\n\n"
        "Para cualquier controversia derivada del presente contrato, las partes se someten a la jurisdicción de los tribunales de {ciudad}.\n\n"
        "En prueba de conformidad, se firman dos (2) ejemplares de un mismo tenor y efecto, en {ciudad}, a los {dia} días del mes de {mes} de {ano}.\n\n"
        "EL CONTRATANTE\n\nFirma: ______________________\nNombre: {contratante}\n\n"
        "EL CONTRATADO\n\nFirma: ______________________\nNombre: {contratado}\n"
    )

    texto = plantilla.format(**datos)

    # Dibujar texto con wrapping simple
    textobj = c.beginText()
    textobj.setTextOrigin(margin_left, y)
    textobj.setLeading(14)
    for line in texto.split('\n'):
        # dividir si la linea es muy larga
        if len(line) > 120:
            # simple wrap
            while len(line) > 120:
                textobj.textLine(line[:120])
                line = line[120:]
            if line:
                textobj.textLine(line)
        else:
            textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()


@rrhh_bp.route('/empleados/<int:empleado_id>/contratos/nuevo', methods=['GET', 'POST'])
@login_required
@role_required(RoleEnum.RRHH)
def contrato_nuevo(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    if request.method == 'POST':
        tipo = request.form.get('tipo_contrato', 'Temporal')
        fecha_inicio_str = request.form.get('fecha_inicio', '')
        fecha_fin_str = request.form.get('fecha_fin', '')
        meses = request.form.get('meses', '0')
        monto = request.form.get('monto', '0')
        periodicidad = request.form.get('periodicidad', 'mensual')
        preaviso = request.form.get('preaviso', '30')

        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

            numero = _generar_numero_contrato(empleado_id)

            datos_pdf = {
                'contratante': request.form.get('contratante_nombre', 'EMPRESA'),
                'direccion_contratante': request.form.get('direccion_contratante', ''),
                'contratado': f"{empleado.nombre} {empleado.apellido}",
                'direccion_contratado': request.form.get('direccion_contratado', empleado.direccion if hasattr(empleado, 'direccion') else ''),
                'ci': request.form.get('ci', getattr(empleado, 'ci', '')),
                'objeto': request.form.get('objeto', 'servicios'),
                'meses': meses,
                'fecha_inicio': fecha_inicio.strftime('%d/%m/%Y') if fecha_inicio else '',
                'fecha_fin': fecha_fin.strftime('%d/%m/%Y') if fecha_fin else '',
                'monto': monto,
                'periodicidad': periodicidad,
                'preaviso': preaviso,
                'ciudad': request.form.get('ciudad', 'Ciudad'),
                'dia': fecha_inicio.day if fecha_inicio else datetime.utcnow().day,
                'mes': fecha_inicio.strftime('%B') if fecha_inicio else datetime.utcnow().strftime('%B'),
                'ano': fecha_inicio.year if fecha_inicio else datetime.utcnow().year
            }

            pdf_bytes = generar_pdf_contrato(datos_pdf)

            contrato = Contrato(
                empleado_id=empleado_id,
                numero_contrato=numero,
                tipo_contrato=tipo,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                contenido=pdf_bytes,
                variables=json.dumps(datos_pdf, default=str)
            )
            db.session.add(contrato)
            db.session.commit()

            registrar_operacion_crud(current_user, 'contratos', 'CREATE', 'contratos', contrato.id, {'numero': numero})
            flash('Contrato generado y guardado correctamente', 'success')
            return redirect(url_for('rrhh.perfil_empleado', empleado_id=empleado_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear contrato: {str(e)}', 'danger')
            return redirect(url_for('rrhh.contrato_nuevo', empleado_id=empleado_id))

    # GET
    return render_template('rrhh/contrato_form.html', empleado=empleado)


@rrhh_bp.route('/contratos/<int:contrato_id>/descargar')
@login_required
@role_required(RoleEnum.RRHH)
def contrato_descargar(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    if not contrato.contenido:
        flash('No hay contenido PDF para este contrato', 'danger')
        return redirect(url_for('rrhh.perfil_empleado', empleado_id=contrato.empleado_id))
    buf = BytesIO(contrato.contenido)
    filename = f"{contrato.numero_contrato}.pdf"
    return send_file(buf, as_attachment=True, download_name=filename, mimetype='application/pdf')


