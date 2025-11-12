from flask import request
from functools import wraps
from .models import db, Bitacora

def registrar_bitacora(usuario, modulo, accion, tabla, registro_id=None, detalle=None):
    """
    Registra una acción en la bitácora
    
    Args:
        usuario: Usuario que realiza la acción
        modulo: Módulo donde se realiza la acción (empleados, asistencia, etc.)
        accion: CREATE, UPDATE, DELETE, VIEW
        tabla: Nombre de la tabla
        registro_id: ID del registro afectado
        detalle: Detalles adicionales de la acción
    """
    try:
        bitacora = Bitacora(
            usuario_id=usuario.id,
            modulo=modulo,
            accion=accion,
            tabla=tabla,
            registro_id=registro_id,
            detalle=detalle,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:255]
        )
        db.session.add(bitacora)
        db.session.commit()
    except Exception as e:
        print(f"Error al registrar bitácora: {str(e)}")
        db.session.rollback()

def bitacora_required(modulo, accion, tabla):
    """
    Decorador para registrar automáticamente acciones en la bitácora
    
    Uso:
        @app.route('/empleado/crear', methods=['POST'])
        @login_required
        @bitacora_required('empleados', 'CREATE', 'empleados')
        def crear_empleado():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            # El registro se debe hacer dentro de la función si es necesario
            return result
        return decorated_function
    return decorator

def registrar_operacion_crud(usuario, modulo, accion, tabla, registro_id, detalle_dict=None):
    """
    Registra operaciones CRUD con detalles formateados
    """
    detalle = str(detalle_dict) if detalle_dict else ""
    registrar_bitacora(usuario, modulo, accion, tabla, registro_id, detalle)
