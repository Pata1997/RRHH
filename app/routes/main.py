from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Empleado, Asistencia, Liquidacion, EstadoEmpleadoEnum
from datetime import date

main_bp = Blueprint('main', __name__)

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
    # Estadísticas
    total_empleados = Empleado.query.count()
    # Use the Enum member for comparison so SQLAlchemy / PostgreSQL receive a valid enum value
    empleados_activos = Empleado.query.filter(Empleado.estado == EstadoEmpleadoEnum.ACTIVO).count()
    
    # Asistencias de hoy
    hoy = date.today()
    asistencias_hoy = Asistencia.query.filter_by(fecha=hoy).count()
    
    # Últimas liquidaciones
    ultima_liquidacion = Liquidacion.query.order_by(Liquidacion.id.desc()).first()
    
    return render_template('dashboard.html',
                           total_empleados=total_empleados,
                           empleados_activos=empleados_activos,
                           asistencias_hoy=asistencias_hoy,
                           ultima_liquidacion=ultima_liquidacion)
