from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

db = SQLAlchemy()

class RoleEnum(Enum):
    RRHH = "RRHH"
    ASISTENTE_RRHH = "Asistente RRHH"

class EstadoEmpleadoEnum(Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    SUSPENDIDO = "Suspendido"
    JUBILADO = "Jubilado"

class EstadoPermisoEnum(Enum):
    PENDIENTE = "Pendiente"
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado"
    COMPLETADO = "Completado"

class EstadoVacacionEnum(Enum):
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"
    COMPLETADA = "Completada"

# ===================== USUARIO =====================
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.Enum(RoleEnum), default=RoleEnum.ASISTENTE_RRHH, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)
    
    # Relaciones
    bitacoras = db.relationship('Bitacora', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'

# ===================== CARGO =====================
# ===================== EMPRESA =====================
class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ruc = db.Column(db.String(20), unique=True)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    logo_path = db.Column(db.String(255))  # Ruta del logo
    razon_social = db.Column(db.String(255))  # Razón social completa
    pais = db.Column(db.String(100), default='Paraguay')
    ciudad = db.Column(db.String(100))
    representante_legal = db.Column(db.String(255))  # Nombre del representante
    ci_representante = db.Column(db.String(20))  # CI del representante
    
    # Configuraciones de cálculos
    porcentaje_ips_empleado = db.Column(db.Numeric(5, 2), default=9.00)  # 9%
    porcentaje_ips_empleador = db.Column(db.Numeric(5, 2), default=16.50)  # 16.5%
    dias_habiles_mes = db.Column(db.Integer, default=30)  # Para cálculo de diarios
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Empresa {self.nombre}>'

# ===================== CARGO =====================
class Cargo(db.Model):
    __tablename__ = 'cargos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    salario_base = db.Column(db.Numeric(12, 2), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    empleados = db.relationship('Empleado', backref='cargo', lazy=True)
    
    def __repr__(self):
        return f'<Cargo {self.nombre}>'

# ===================== EMPLEADO =====================
class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    ci = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.String(20))
    
    # Datos laborales
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    salario_base = db.Column(db.Numeric(12, 2), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_retiro = db.Column(db.Date)
    estado = db.Column(db.Enum(EstadoEmpleadoEnum), default=EstadoEmpleadoEnum.ACTIVO)
    
    # Datos personales
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(1))  # M/F
    direccion = db.Column(db.String(255))
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    asistencias = db.relationship('Asistencia', backref='empleado', lazy=True, cascade='all, delete-orphan')
    # Eventos de asistencia (punches)
    asistencia_eventos = db.relationship('AsistenciaEvento', backref='empleado', lazy=True, cascade='all, delete-orphan')
    permisos = db.relationship('Permiso', backref='empleado', lazy=True, cascade='all, delete-orphan')
    sanciones = db.relationship('Sancion', backref='empleado', lazy=True, cascade='all, delete-orphan')
    contratos = db.relationship('Contrato', backref='empleado', lazy=True, cascade='all, delete-orphan')
    ingresos_extras = db.relationship('IngresoExtra', backref='empleado', lazy=True, cascade='all, delete-orphan')
    descuentos = db.relationship('Descuento', backref='empleado', lazy=True, cascade='all, delete-orphan')
    liquidaciones = db.relationship('Liquidacion', backref='empleado', lazy=True, cascade='all, delete-orphan')
    vacaciones = db.relationship('Vacacion', backref='empleado', lazy=True, cascade='all, delete-orphan')
    anticipos = db.relationship('Anticipo', backref='empleado', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Empleado {self.codigo} - {self.nombre} {self.apellido}>'
    
    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    @property
    def antiguedad_texto(self):
        """Calcula antiguedad en formato 'X años y Y meses'"""
        if not self.fecha_ingreso:
            return "N/A"
        
        today = date.today()
        años = today.year - self.fecha_ingreso.year
        meses = today.month - self.fecha_ingreso.month
        
        if meses < 0:
            años -= 1
            meses += 12
        
        if años == 0 and meses == 0:
            dias = (today - self.fecha_ingreso).days
            return f"{dias} días"
        elif años == 0:
            return f"{meses} mes{'es' if meses != 1 else ''}"
        elif meses == 0:
            return f"{años} año{'s' if años != 1 else ''}"
        else:
            return f"{años} año{'s' if años != 1 else ''} y {meses} mes{'es' if meses != 1 else ''}"
    
    @property
    def antiguedad_dias(self):
        """Retorna total de días desde ingreso"""
        if not self.fecha_ingreso:
            return 0
        return (date.today() - self.fecha_ingreso).days

# ===================== CONTRATO =====================
class Contrato(db.Model):
    __tablename__ = 'contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    numero_contrato = db.Column(db.String(50), unique=True, nullable=False)
    tipo_contrato = db.Column(db.String(50))  # Permanente, Temporal, etc.
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    contenido = db.Column(db.LargeBinary)  # PDF almacenado
    variables = db.Column(db.Text, nullable=True)  # JSON string con las variables usadas para generar el PDF
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contrato {self.numero_contrato}>'

# ===================== ASISTENCIA =====================
class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, index=True)
    hora_entrada = db.Column(db.Time)
    hora_salida = db.Column(db.Time)
    presente = db.Column(db.Boolean, default=True)
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('empleado_id', 'fecha', name='uq_empleado_fecha'),)
    
    def __repr__(self):
        return f'<Asistencia {self.empleado.codigo} - {self.fecha}>'


# ===================== ASISTENCIA EVENTOS =====================
class AsistenciaEvento(db.Model):
    """Registra cada punch (entrada/salida) con timestamp para luego resumir por día."""
    __tablename__ = 'asistencia_eventos'

    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    ts = db.Column(db.DateTime, nullable=False, index=True)
    tipo = db.Column(db.String(10), nullable=False)  # 'in' o 'out'
    origen = db.Column(db.String(50), default='web')
    detalles = db.Column(db.Text, nullable=True)  # JSON con ip, user_agent, etc.
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AsistenciaEvento {self.empleado_id} - {self.ts} - {self.tipo}>'

# ===================== PERMISO =====================
class Permiso(db.Model):
    __tablename__ = 'permisos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo_permiso = db.Column(db.String(50), nullable=False)  # Enfermedad, Asunto personal, etc.
    motivo = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    dias_solicitados = db.Column(db.Integer)
    estado = db.Column(db.Enum(EstadoPermisoEnum), default=EstadoPermisoEnum.PENDIENTE)
    # Nuevo: indica si el permiso tiene goce salarial (True) o no (False)
    con_goce = db.Column(db.Boolean, default=False)
    # Si se genera un descuento automático al aprobar, lo vinculamos aquí
    descuento_id = db.Column(db.Integer, db.ForeignKey('descuentos.id'), nullable=True)
    justificativo_archivo = db.Column(db.String(255))
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permiso {self.empleado.codigo} - {self.tipo_permiso}>'

# ===================== SANCION =====================
class Sancion(db.Model):
    __tablename__ = 'sanciones'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo_sancion = db.Column(db.String(50), nullable=False)  # Amonestación, Descuento, etc.
    motivo = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Numeric(12, 2), default=0)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.Text)
    # Ruta al archivo justificativo (imagen/PDF) asociado a la sanción
    justificativo_archivo = db.Column(db.String(255), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Sancion {self.empleado.codigo} - {self.tipo_sancion}>'

# ===================== INGRESO EXTRA =====================
class IngresoExtra(db.Model):
    __tablename__ = 'ingresos_extras'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Bonificación, Aguinaldo, etc.
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    mes = db.Column(db.Integer)  # 1-12
    año = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    # Estado y control de aplicación
    estado = db.Column(db.String(20), default='PENDIENTE')  # PENDIENTE, APROBADO, RECHAZADO, APLICADO
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    aplicado = db.Column(db.Boolean, default=False)
    fecha_aplicacion = db.Column(db.DateTime, nullable=True)
    justificativo_archivo = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<IngresoExtra {self.empleado.codigo} - {self.tipo}>'


# ===================== HORAS EXTRA =====================
class HorasExtra(db.Model):
    __tablename__ = 'horas_extras'

    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, index=True)
    horas = db.Column(db.Numeric(6, 2), nullable=False)  # horas en formato decimal, aceptar minutos
    monto_calculado = db.Column(db.Numeric(12, 2), nullable=False)
    origen = db.Column(db.String(50), default='asistencia')
    estado = db.Column(db.String(20), default='PENDIENTE')  # PENDIENTE, APROBADO, RECHAZADO, EXPIRADO
    aprobado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha_aprobacion = db.Column(db.DateTime, nullable=True)
    aplicado = db.Column(db.Boolean, default=False)
    fecha_aplicacion = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HorasExtra {self.empleado_id} - {self.fecha} - {self.horas}h>'

# ===================== DESCUENTO =====================
class Descuento(db.Model):
    __tablename__ = 'descuentos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # IPS, Adelanto, etc.
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    mes = db.Column(db.Integer)
    año = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    # Nuevo: activo permite marcar descuentos anulados sin borrar el registro
    activo = db.Column(db.Boolean, default=True)
    # Origen para trazabilidad (permiso, sancion, manual)
    origen_tipo = db.Column(db.String(50))
    origen_id = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Descuento {self.empleado.codigo} - {self.tipo}>'


# ===================== ANTICIPO =====================
class Anticipo(db.Model):
    __tablename__ = 'anticipos'

    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    aprobado = db.Column(db.Boolean, default=False)
    aprobado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha_aprobacion = db.Column(db.DateTime, nullable=True)
    rechazado = db.Column(db.Boolean, default=False)
    rechazado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha_rechazo = db.Column(db.DateTime, nullable=True)
    aplicado = db.Column(db.Boolean, default=False)
    fecha_aplicacion = db.Column(db.Date, nullable=True)
    justificativo_archivo = db.Column(db.String(255), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Anticipo {self.empleado_id} - {self.monto} - Aprobado:{self.aprobado} - Rechazado:{self.rechazado}>'

# ===================== LIQUIDACION =====================
class Liquidacion(db.Model):
    __tablename__ = 'liquidaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    periodo = db.Column(db.String(10), nullable=False)  # YYYY-MM
    salario_base = db.Column(db.Numeric(12, 2), nullable=False)
    ingresos_extras = db.Column(db.Numeric(12, 2), default=0)
    descuentos = db.Column(db.Numeric(12, 2), default=0)
    aporte_ips = db.Column(db.Numeric(12, 2), default=0)  # 9.625%
    salario_neto = db.Column(db.Numeric(12, 2), nullable=False)
    dias_trabajados = db.Column(db.Integer)
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_content = db.Column(db.LargeBinary)
    
    # Campos para liquidación por despido
    despido_id = db.Column(db.Integer, db.ForeignKey('despidos.id'), nullable=True)
    despido = db.relationship('Despido', foreign_keys=[despido_id], backref='liquidaciones')
    
    # Desglose de rubros en despido
    indemnizacion_monto = db.Column(db.Numeric(12, 2), default=0)
    aguinaldo_monto = db.Column(db.Numeric(12, 2), default=0)
    vacaciones_monto = db.Column(db.Numeric(12, 2), default=0)
    aportes_ips_despido = db.Column(db.Numeric(12, 2), default=0)
    
    def __repr__(self):
        return f'<Liquidacion {self.empleado.codigo} - {self.periodo}>'

# ===================== DESPIDO =====================
class Despido(db.Model):
    __tablename__ = 'despidos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    empleado = db.relationship('Empleado', backref='despidos', foreign_keys=[empleado_id])
    
    # Tipo: 'justificado' o 'injustificado'
    tipo = db.Column(db.String(50), nullable=False)
    
    # Causal legal (si justificado)
    causal = db.Column(db.String(100), nullable=True)
    
    # Descripción
    descripcion = db.Column(db.Text, nullable=True)
    
    # Fecha del despido
    fecha_despido = db.Column(db.Date, nullable=False)
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    usuario = db.relationship('Usuario', foreign_keys=[usuario_id])
    
    def __repr__(self):
        return f"<Despido {self.empleado.nombre} - {self.tipo}>"

# ===================== VACACION =====================
class Vacacion(db.Model):
    __tablename__ = 'vacaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    año = db.Column(db.Integer, nullable=False)
    dias_disponibles = db.Column(db.Integer, default=15)
    dias_tomados = db.Column(db.Integer, default=0)
    dias_pendientes = db.Column(db.Integer, default=15)
    fecha_inicio_solicitud = db.Column(db.Date)
    fecha_fin_solicitud = db.Column(db.Date)
    estado = db.Column(db.Enum(EstadoVacacionEnum), default=EstadoVacacionEnum.PENDIENTE)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Vacacion {self.empleado.codigo} - {self.año}>'

# ===================== BITACORA =====================
class Bitacora(db.Model):
    __tablename__ = 'bitacora'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    modulo = db.Column(db.String(50), nullable=False)  # empleados, asistencia, permisos, etc.
    accion = db.Column(db.String(50), nullable=False)  # CREATE, UPDATE, DELETE, VIEW
    tabla = db.Column(db.String(50), nullable=False)
    registro_id = db.Column(db.Integer)  # ID del registro afectado
    detalle = db.Column(db.Text)  # Detalles de la acción
    ip_address = db.Column(db.String(45))  # IPv4 o IPv6
    user_agent = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Bitacora {self.usuario.nombre_usuario} - {self.accion} en {self.modulo}>'

# ===================== DETALLE LIQUIDACION =====================
class DetalleLiquidacion(db.Model):
    """Desglose itemizado de rubros en una liquidación"""
    __tablename__ = 'detalles_liquidacion'
    
    id = db.Column(db.Integer, primary_key=True)
    liquidacion_id = db.Column(db.Integer, db.ForeignKey('liquidaciones.id'), nullable=False)
    liquidacion = db.relationship('Liquidacion', backref='detalles')
    
    # Tipo de rubro: 'salario_base', 'extras', 'descuentos', 'aporte_ips'
    tipo_rubro = db.Column(db.String(50), nullable=False)
    
    # Descripción del rubro (ej: "Bonificación por antigüedad", "Adelanto de sueldo")
    descripcion = db.Column(db.String(255), nullable=False)
    
    # Monto
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Porcentaje (para aportes): ej 9.625% IPS
    porcentaje = db.Column(db.Numeric(5, 3), default=0)
    
    def __repr__(self):
        return f'<DetalleLiquidacion {self.tipo_rubro} - {self.monto}>'

# ===================== FAMILIAR EMPLEADO =====================
class FamiliarEmpleado(db.Model):
    """Registro de familiares/dependientes para bonificación familiar"""
    __tablename__ = 'familiares_empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    empleado = db.relationship('Empleado', backref='familiares')
    
    nombre = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Hijo, Esposa/Esposo, Padre/Madre
    fecha_nacimiento = db.Column(db.Date)
    ci = db.Column(db.String(20))
    
    # Vigencia
    activo = db.Column(db.Boolean, default=True)
    fecha_inicio = db.Column(db.Date, default=date.today)
    fecha_fin = db.Column(db.Date, nullable=True)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FamiliarEmpleado {self.nombre} de {self.empleado.nombre}>'

# ===================== BONIFICACION FAMILIAR =====================
class BonificacionFamiliar(db.Model):
    """Registro de bonificaciones por familiares/dependientes por mes"""
    __tablename__ = 'bonificaciones_familiares'
    
    id = db.Column(db.Integer, primary_key=True)
    liquidacion_id = db.Column(db.Integer, db.ForeignKey('liquidaciones.id'), nullable=False)
    liquidacion = db.relationship('Liquidacion', backref='bonificaciones_familiares')
    
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    empleado = db.relationship('Empleado', backref='bonificaciones_familiares')
    
    familiar_id = db.Column(db.Integer, db.ForeignKey('familiares_empleados.id'), nullable=False)
    familiar = db.relationship('FamiliarEmpleado')
    
    # Monto por dependiente (configurable por empresa, ej: 50000 Gs.)
    monto_unitario = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Mes/Año de aplicación
    mes = db.Column(db.Integer)  # 1-12
    año = db.Column(db.Integer)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BonificacionFamiliar {self.empleado.codigo} - {self.monto_unitario}>'

# ===================== POSTULANTE =====================
class Postulante(db.Model):
    """Postulante a vacantes (módulo de reclutamiento)"""
    __tablename__ = 'postulantes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Datos personales
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    
    # Información personal adicional
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    nivel_academico = db.Column(db.String(120), nullable=True)  # Primaria, Secundaria, Terciaria, Universitaria, Postgrado
    
    # Información laboral
    cargo_postulado = db.Column(db.String(120), nullable=False)
    experiencia_años = db.Column(db.Integer, default=0)
    
    # Salario esperado
    salario_esperado = db.Column(db.Numeric(12, 2), nullable=True)
    
    # Fecha de postulación
    fecha_postulacion = db.Column(db.Date, nullable=False, default=date.today)
    
    # Estado del postulante: 'Nuevo', 'En Evaluación', 'Contratado', 'Rechazado', 'En Espera'
    estado = db.Column(db.String(50), default='Nuevo')
    
    # Observaciones
    observaciones = db.Column(db.Text)
    
    # Si fue contratado, referencia al empleado creado
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=True)
    empleado = db.relationship('Empleado')
    
    # Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizado = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Postulante {self.nombre} {self.apellido} - {self.cargo_postulado}>'

# ===================== DOCUMENTOS CURRICULUM =====================
class DocumentosCurriculum(db.Model):
    """Documentos de un postulante (CV, certificados, etc.)"""
    __tablename__ = 'documentos_curriculum'
    
    id = db.Column(db.Integer, primary_key=True)
    postulante_id = db.Column(db.Integer, db.ForeignKey('postulantes.id'), nullable=False)
    postulante = db.relationship('Postulante', backref='documentos')
    
    tipo = db.Column(db.String(50), nullable=False)  # CV, Certificado, Portafolio, etc.
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)  # Ruta relativa en app/uploads/postulantes/
    
    # Metadata
    tamaño_bytes = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    
    # Auditoría
    fecha_carga = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DocumentosCurriculum {self.postulante.nombre} - {self.tipo}>'
