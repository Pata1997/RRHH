from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..models import db, Usuario, RoleEnum
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        password = request.form.get('password')
        
        if not nombre_usuario or not password:
            flash('Usuario y contraseña son requeridos', 'danger')
            return redirect(url_for('auth.login'))
        
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        
        if usuario and usuario.check_password(password) and usuario.activo:
            login_user(usuario, remember=request.form.get('recuerdame'))
            usuario.ultimo_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'¡Bienvenido {usuario.nombre_completo}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña inválidos, o la cuenta está inactiva', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Ruta de logout"""
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """Cambiar contraseña del usuario actual"""
    if request.method == 'POST':
        password_actual = request.form.get('password_actual')
        password_nuevo = request.form.get('password_nuevo')
        password_confirmacion = request.form.get('password_confirmacion')
        
        # Validaciones
        if not password_actual or not password_nuevo or not password_confirmacion:
            flash('Todos los campos son requeridos', 'danger')
            return redirect(url_for('auth.cambiar_password'))
        
        if not current_user.check_password(password_actual):
            flash('La contraseña actual es incorrecta', 'danger')
            return redirect(url_for('auth.cambiar_password'))
        
        if password_nuevo != password_confirmacion:
            flash('Las contraseñas nuevas no coinciden', 'danger')
            return redirect(url_for('auth.cambiar_password'))
        
        if len(password_nuevo) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return redirect(url_for('auth.cambiar_password'))
        
        current_user.set_password(password_nuevo)
        db.session.commit()
        
        flash('Contraseña actualizada exitosamente', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/cambiar_password.html')
