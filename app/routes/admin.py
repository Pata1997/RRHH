"""
Rutas administrativas - Solo accesibles para el rol ADMIN
Gestión de usuarios del sistema
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Usuario, RoleEnum
from app.bitacora import registrar_bitacora
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorador para verificar que el usuario sea ADMIN"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.rol != RoleEnum.ADMIN:
            flash('No tienes permisos para acceder a esta sección.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/usuarios')
@login_required
def listar_usuarios():
    """Lista todos los usuarios del sistema"""
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    
    registrar_bitacora(
        current_user, 'usuarios', 'VIEW', 'usuarios',
        detalle='Listado de usuarios'
    )
    
    return render_template('admin/usuarios.html', usuarios=usuarios)


@admin_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        try:
            nombre_usuario = request.form.get('nombre_usuario').strip()
            email = request.form.get('email').strip()
            nombre_completo = request.form.get('nombre_completo').strip()
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            rol = request.form.get('rol')
            activo = request.form.get('activo') == 'on'
            
            # Validaciones
            if not all([nombre_usuario, email, nombre_completo, password, rol]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('admin.crear_usuario'))
            
            if password != password_confirm:
                flash('Las contraseñas no coinciden.', 'danger')
                return redirect(url_for('admin.crear_usuario'))
            
            if len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
                return redirect(url_for('admin.crear_usuario'))
            
            # Verificar si ya existe el usuario o email
            if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
                flash(f'El nombre de usuario "{nombre_usuario}" ya existe.', 'danger')
                return redirect(url_for('admin.crear_usuario'))
            
            if Usuario.query.filter_by(email=email).first():
                flash(f'El email "{email}" ya está registrado.', 'danger')
                return redirect(url_for('admin.crear_usuario'))
            
            # Crear usuario
            nuevo_usuario = Usuario(
                nombre_usuario=nombre_usuario,
                email=email,
                nombre_completo=nombre_completo,
                rol=RoleEnum[rol],
                activo=activo
            )
            nuevo_usuario.set_password(password)
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            registrar_bitacora(
                current_user, 'usuarios', 'CREATE', 'usuarios',
                registro_id=nuevo_usuario.id,
                detalle=f'Usuario creado: {nombre_usuario} ({rol})'
            )
            
            flash(f'Usuario "{nombre_usuario}" creado exitosamente.', 'success')
            return redirect(url_for('admin.listar_usuarios'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear usuario: {str(e)}', 'danger')
            return redirect(url_for('admin.crear_usuario'))
    
    return render_template('admin/crear_usuario.html', roles=RoleEnum)


@admin_bp.route('/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    """Editar un usuario existente"""
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        try:
            nombre_usuario = request.form.get('nombre_usuario').strip()
            email = request.form.get('email').strip()
            nombre_completo = request.form.get('nombre_completo').strip()
            rol = request.form.get('rol')
            activo = request.form.get('activo') == 'on'
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            # Validaciones
            if not all([nombre_usuario, email, nombre_completo, rol]):
                flash('Todos los campos son obligatorios.', 'danger')
                return redirect(url_for('admin.editar_usuario', usuario_id=usuario_id))
            
            # Verificar duplicados (excepto el mismo usuario)
            usuario_existente = Usuario.query.filter(
                Usuario.nombre_usuario == nombre_usuario,
                Usuario.id != usuario_id
            ).first()
            if usuario_existente:
                flash(f'El nombre de usuario "{nombre_usuario}" ya existe.', 'danger')
                return redirect(url_for('admin.editar_usuario', usuario_id=usuario_id))
            
            email_existente = Usuario.query.filter(
                Usuario.email == email,
                Usuario.id != usuario_id
            ).first()
            if email_existente:
                flash(f'El email "{email}" ya está registrado.', 'danger')
                return redirect(url_for('admin.editar_usuario', usuario_id=usuario_id))
            
            # Actualizar datos
            usuario.nombre_usuario = nombre_usuario
            usuario.email = email
            usuario.nombre_completo = nombre_completo
            usuario.rol = RoleEnum[rol]
            usuario.activo = activo
            
            # Cambiar contraseña solo si se proporciona
            if password:
                if password != password_confirm:
                    flash('Las contraseñas no coinciden.', 'danger')
                    return redirect(url_for('admin.editar_usuario', usuario_id=usuario_id))
                
                if len(password) < 6:
                    flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
                    return redirect(url_for('admin.editar_usuario', usuario_id=usuario_id))
                
                usuario.set_password(password)
            
            db.session.commit()
            
            registrar_bitacora(
                current_user, 'usuarios', 'UPDATE', 'usuarios',
                registro_id=usuario.id,
                detalle=f'Usuario actualizado: {nombre_usuario}'
            )
            
            flash(f'Usuario "{nombre_usuario}" actualizado exitosamente.', 'success')
            return redirect(url_for('admin.listar_usuarios'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar usuario: {str(e)}', 'danger')
            return redirect(url_for('admin.editar_usuario', usuario_id=usuario_id))
    
    return render_template('admin/editar_usuario.html', usuario=usuario, roles=RoleEnum)


@admin_bp.route('/usuarios/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
def eliminar_usuario(usuario_id):
    """Eliminar un usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # No permitir eliminar el propio usuario
    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario.', 'danger')
        return redirect(url_for('admin.listar_usuarios'))
    
    # No permitir eliminar si es el único admin
    if usuario.rol == RoleEnum.ADMIN:
        admins_count = Usuario.query.filter_by(rol=RoleEnum.ADMIN).count()
        if admins_count <= 1:
            flash('No puedes eliminar el único administrador del sistema.', 'danger')
            return redirect(url_for('admin.listar_usuarios'))
    
    try:
        nombre = usuario.nombre_usuario
        
        db.session.delete(usuario)
        db.session.commit()
        
        registrar_bitacora(
            current_user, 'usuarios', 'DELETE', 'usuarios',
            registro_id=usuario_id,
            detalle=f'Usuario eliminado: {nombre}'
        )
        
        flash(f'Usuario "{nombre}" eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'danger')
    
    return redirect(url_for('admin.listar_usuarios'))


@admin_bp.route('/usuarios/<int:usuario_id>/toggle-estado', methods=['POST'])
@login_required
def toggle_estado_usuario(usuario_id):
    """Activar/Desactivar un usuario"""
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # No permitir desactivar el propio usuario
    if usuario.id == current_user.id:
        flash('No puedes desactivar tu propio usuario.', 'danger')
        return redirect(url_for('admin.listar_usuarios'))
    
    try:
        usuario.activo = not usuario.activo
        estado = 'activado' if usuario.activo else 'desactivado'
        
        db.session.commit()
        
        registrar_bitacora(
            current_user, 'usuarios', 'UPDATE', 'usuarios',
            registro_id=usuario.id,
            detalle=f'Usuario {estado}: {usuario.nombre_usuario}'
        )
        
        flash(f'Usuario "{usuario.nombre_usuario}" {estado} exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'danger')
    
    return redirect(url_for('admin.listar_usuarios'))
