from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .config import config
from .models import db, Usuario
import os
import warnings
from sqlalchemy.exc import SAWarning

# Suprimir warning de tabla duplicada en modo debug
warnings.filterwarnings('ignore', 
                       message='.*already contains a class with the same class name.*',
                       category=SAWarning)

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
    
    # Registrar filtro personalizado para formato de guaraníes
    @app.template_filter('gs')
    def formato_guaranies(valor):
        """Formatea números con separador de miles (punto) para guaraníes
        Ejemplos: 1000 -> 1.000 | 1000000 -> 1.000.000
        """
        try:
            if valor is None:
                return '0'
            # Convertir a float y formatear
            numero = float(valor)
            # Formatear con comas y luego reemplazar por puntos
            return '{:,.0f}'.format(numero).replace(',', '.')
        except (ValueError, TypeError):
            return str(valor)
    
    # Context processor para empresa (disponible en todos los templates)
    @app.context_processor
    def inject_empresa():
        """Inyecta la información de la empresa en todos los templates"""
        from .models import Empresa
        empresa = Empresa.query.first()
        return dict(empresa_global=empresa)
    
    # Registrar blueprints
    from .routes.auth import auth_bp
    from .routes.rrhh import rrhh_bp
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(rrhh_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Configurar APScheduler para cierre automático de asistencias
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        from flask_apscheduler import APScheduler
        from .routes.rrhh import cerrar_asistencias_automatico
        from datetime import date
        
        scheduler = APScheduler()
        scheduler.init_app(app)
        
        @scheduler.task('cron', id='cerrar_asistencias_diarias', hour=17, minute=30)
        def tarea_cerrar_asistencias():
            """Tarea programada: cierra asistencias a las 17:30 todos los días"""
            with app.app_context():
                try:
                    print(f"\n🕐 Ejecutando cierre automático de asistencias - {date.today()}")
                    stats = cerrar_asistencias_automatico()
                    print(f"✅ {stats['mensaje']}")
                    print(f"   Procesados: {stats['procesados']} | Vacaciones: {stats['vacaciones']} | "
                          f"Permisos: {stats['permisos']} | Ausencias: {stats['ausencias']}")
                except Exception as e:
                    print(f"❌ Error en cierre automático: {e}")
        
        scheduler.start()
        print("📅 Scheduler iniciado: Cierre automático de asistencias programado para las 17:30")

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
