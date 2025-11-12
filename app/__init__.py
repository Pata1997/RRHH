from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .config import config
from .models import db, Usuario
import os

def create_app(config_name=None):
    """Factory para crear la aplicación Flask"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Inicializar CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Configurar Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Crear directorio de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Registrar blueprints
    from .routes.auth import auth_bp
    from .routes.rrhh import rrhh_bp
    from .routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(rrhh_bp)
    app.register_blueprint(main_bp)

    # Crear tablas (capturar errores de conexión / encoding para diagnóstico)
    with app.app_context():
        try:
            db.create_all()
        except UnicodeDecodeError as ude:
            print("ERROR: UnicodeDecodeError al conectar con la base de datos:", ude)
            print("Revisa que las variables de entorno (DATABASE_URL, PGPASSWORD, etc.) estén en UTF-8 y no tengan caracteres acentuados.")
            # Mostrar variables relevantes para diagnóstico (repr)
            try:
                keys = ['DATABASE_URL', 'PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD', 'PGDATABASE']
                for k in keys:
                    print(f"DEBUG ENV {k} repr:", repr(os.environ.get(k)))
            except Exception:
                pass
            # En modo desarrollo, continuar sin fallar (para permitir testing con SQLite)
            if app.debug:
                print("⚠️  Continuando en modo desarrollo sin crear tablas en PostgreSQL")
            else:
                raise
        except Exception as e:
            print(f"⚠️  Advertencia al crear tablas: {type(e).__name__}: {str(e)}")
            # En modo desarrollo, continuar; en producción, re-raise
            if not app.debug:
                raise
    
    return app
