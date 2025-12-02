from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Empleado, Asistencia, Liquidacion, EstadoEmpleadoEnum, db
from datetime import date, timedelta

main_bp = Blueprint('main', __name__)

def verificar_y_crear_ausencias_retroactivas():
    """
    Verifica días sin registros de asistencia y crea ausencias pendientes
    para empleados activos. Solo procesa hasta 7 días atrás.
    """
    hoy = date.today()
    
    # Buscar la última fecha con asistencias registradas
    ultima_asistencia = Asistencia.query.order_by(Asistencia.fecha.desc()).first()
    
    print(f"🔍 DEBUG - Verificando ausencias retroactivas...")
    print(f"   Hoy: {hoy}")
    
    if not ultima_asistencia:
        print(f"   ❌ No hay asistencias previas en el sistema")
        return 0  # Primera vez, no hay datos históricos
    
    print(f"   Última asistencia: {ultima_asistencia.fecha} (Empleado: {ultima_asistencia.empleado.nombre_completo})")
    
    fecha_desde = ultima_asistencia.fecha + timedelta(days=1)
    print(f"   Fecha desde: {fecha_desde}")
    
    # Solo procesar hasta 7 días atrás como máximo
    fecha_minima = hoy - timedelta(days=7)
    if fecha_desde < fecha_minima:
        print(f"   ⚠️ Ajustando fecha_desde de {fecha_desde} a {fecha_minima} (límite 7 días)")
        fecha_desde = fecha_minima
    
    # Si ya estamos al día, no hacer nada
    if fecha_desde >= hoy:
        print(f"   ✅ Sistema al día - No hay días faltantes")
        return 0
    
    print(f"   📅 Procesando desde {fecha_desde} hasta {hoy}")
    
    # Para cada día faltante (solo días hábiles: lunes a viernes)
    dias_procesados = 0
    fecha_actual = fecha_desde
    
    print(f"   🔄 Iniciando loop de verificación...")
    
    while fecha_actual < hoy:
        # Solo lunes a viernes (0=lunes, 4=viernes, 5=sábado, 6=domingo)
        if fecha_actual.weekday() < 5:
            print(f"      Verificando {fecha_actual.strftime('%d/%m/%Y - %A')}...")
            empleados_activos = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
            print(f"         {len(empleados_activos)} empleados activos")
            
            ausencias_dia = 0
            for empleado in empleados_activos:
                # Verificar si ya tiene registro ese día
                existe = Asistencia.query.filter_by(
                    empleado_id=empleado.id,
                    fecha=fecha_actual
                ).first()
                
                if not existe:
                    # Crear ausencia pendiente
                    ausencia = Asistencia(
                        empleado_id=empleado.id,
                        fecha=fecha_actual,
                        presente=False,
                        hora_entrada=None,
                        hora_salida=None,
                        observaciones='Ausencia sin registro - Sistema no operativo',
                        justificacion_estado='PENDIENTE'
                    )
                    db.session.add(ausencia)
                    dias_procesados += 1
                    ausencias_dia += 1
            
            print(f"         ✓ {ausencias_dia} ausencias creadas para este día")
        else:
            print(f"      Saltando {fecha_actual.strftime('%d/%m/%Y - %A')} (fin de semana)")
        
        fecha_actual += timedelta(days=1)
    
    if dias_procesados > 0:
        db.session.commit()
        print(f"✅ Creadas {dias_procesados} ausencias retroactivas de días faltantes")
    else:
        print(f"   ℹ️ No se crearon ausencias (todos los días tienen registro)")
    
    return dias_procesados

@main_bp.route('/')
def index():
    """Página de inicio"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    # Verificar y crear ausencias de días que el sistema estuvo apagado
    try:
        ausencias_creadas = verificar_y_crear_ausencias_retroactivas()
        if ausencias_creadas > 0:
            print(f"🔔 Se detectaron {ausencias_creadas} ausencias de días anteriores")
    except Exception as e:
        print(f"⚠️ Error al verificar ausencias retroactivas: {str(e)}")
    
    # Estadísticas
    total_empleados = Empleado.query.count()
    # Use the Enum member for comparison so SQLAlchemy / PostgreSQL receive a valid enum value
    empleados_activos = Empleado.query.filter(Empleado.estado == EstadoEmpleadoEnum.ACTIVO).count()
    
    # Asistencias de hoy
    hoy = date.today()
    asistencias_hoy = Asistencia.query.filter_by(fecha=hoy).count()
    
    # Últimas liquidaciones
    ultima_liquidacion = Liquidacion.query.order_by(Liquidacion.id.desc()).first()
    
    # 🚨 AUSENCIAS PENDIENTES DE JUSTIFICACIÓN
    # Buscar todas las ausencias con estado PENDIENTE (sin importar la fecha)
    ausencias_pendientes = Asistencia.query.filter(
        Asistencia.presente == False,
        Asistencia.justificacion_estado == 'PENDIENTE'
    ).order_by(Asistencia.fecha.desc()).all()
    
    return render_template('dashboard.html',
                           total_empleados=total_empleados,
                           empleados_activos=empleados_activos,
                           asistencias_hoy=asistencias_hoy,
                           ultima_liquidacion=ultima_liquidacion,
                           ausencias_pendientes=ausencias_pendientes)
