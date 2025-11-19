"""
Script para RECREAR tablas de Bonificación Familiar
Elimina tablas existentes y las crea correctamente
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from sqlalchemy import text

def recrear_tablas():
    """Elimina y recrea las tablas de bonificación familiar"""
    app = create_app('development')
    
    with app.app_context():
        print("=" * 60)
        print("RECREACIÓN: Bonificación Familiar")
        print("=" * 60)
        
        # Detectar tipo de base de datos
        db_url = str(db.engine.url)
        es_sqlite = 'sqlite' in db_url.lower()
        es_postgres = 'postgres' in db_url.lower()
        
        print(f"\n📊 Base de datos detectada: {'SQLite' if es_sqlite else 'PostgreSQL' if es_postgres else 'Desconocida'}")
        
        try:
            # 1. ELIMINAR tablas existentes
            print("\n[1/6] Eliminando tablas existentes...")
            
            # Para SQLite, usar sintaxis sin CASCADE
            if es_sqlite:
                try:
                    db.session.execute(text("DROP TABLE IF EXISTS bonificaciones_familiares"))
                    print("   ✅ Tabla bonificaciones_familiares eliminada")
                except Exception as e:
                    print(f"   ℹ️  Error: {e}")
                    db.session.rollback()
                
                try:
                    db.session.execute(text("DROP TABLE IF EXISTS salarios_minimos"))
                    print("   ✅ Tabla salarios_minimos eliminada")
                except Exception as e:
                    print(f"   ℹ️  Error: {e}")
                    db.session.rollback()
            else:
                # PostgreSQL con CASCADE
                try:
                    db.session.execute(text("DROP TABLE IF EXISTS bonificaciones_familiares CASCADE"))
                    print("   ✅ Tabla bonificaciones_familiares eliminada")
                except Exception as e:
                    print(f"   ℹ️  Error: {e}")
                    db.session.rollback()
                
                try:
                    db.session.execute(text("DROP TABLE IF EXISTS salarios_minimos CASCADE"))
                    print("   ✅ Tabla salarios_minimos eliminada")
                except Exception as e:
                    print(f"   ℹ️  Error: {e}")
                    db.session.rollback()
                
                try:
                    db.session.execute(text("DROP TYPE IF EXISTS tipohijoenum CASCADE"))
                    print("   ✅ ENUM tipohijoenum eliminado")
                except Exception as e:
                    print(f"   ℹ️  ENUM no existía")
                    db.session.rollback()
            
            db.session.commit()
            
            # 2. CREAR tabla salarios_minimos
            print("\n[2/6] Creando tabla 'salarios_minimos'...")
            if es_sqlite:
                db.session.execute(text("""
                    CREATE TABLE salarios_minimos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        año INTEGER NOT NULL,
                        monto DECIMAL(12, 2) NOT NULL,
                        vigencia_desde DATE NOT NULL,
                        vigencia_hasta DATE,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        usuario_creador_id INTEGER REFERENCES usuarios(id)
                    )
                """))
            else:
                db.session.execute(text("""
                    CREATE TABLE salarios_minimos (
                        id SERIAL PRIMARY KEY,
                        año INTEGER NOT NULL,
                        monto NUMERIC(12, 2) NOT NULL,
                        vigencia_desde DATE NOT NULL,
                        vigencia_hasta DATE,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        usuario_creador_id INTEGER REFERENCES usuarios(id)
                    )
                """))
            db.session.commit()
            print("   ✅ Tabla 'salarios_minimos' creada")
            
            # 3. CREAR enum tipohijoenum (solo PostgreSQL)
            if es_postgres:
                print("\n[3/6] Creando ENUM 'tipohijoenum'...")
                db.session.execute(text("""
                    CREATE TYPE tipohijoenum AS ENUM (
                        'Menor de 18 años',
                        'Mayor de 18 años - Estudiante',
                        'Hijo con discapacidad'
                    )
                """))
                db.session.commit()
                print("   ✅ ENUM 'tipohijoenum' creado")
            else:
                print("\n[3/6] Saltando ENUM (SQLite no soporta ENUMs)")
            
            # 4. CREAR tabla bonificaciones_familiares
            print("\n[4/6] Creando tabla 'bonificaciones_familiares'...")
            if es_sqlite:
                db.session.execute(text("""
                    CREATE TABLE bonificaciones_familiares (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        empleado_id INTEGER NOT NULL REFERENCES empleados(id) ON DELETE CASCADE,
                        hijo_nombre VARCHAR(120) NOT NULL,
                        hijo_apellido VARCHAR(120) NOT NULL,
                        hijo_ci VARCHAR(20),
                        hijo_fecha_nacimiento DATE NOT NULL,
                        sexo VARCHAR(1),
                        tipo VARCHAR(50) NOT NULL DEFAULT 'Menor de 18 años',
                        certificado_nacimiento VARCHAR(500),
                        certificado_estudio VARCHAR(500),
                        certificado_discapacidad VARCHAR(500),
                        activo BOOLEAN DEFAULT 1,
                        fecha_registro DATE DEFAULT CURRENT_DATE,
                        fecha_baja DATE,
                        motivo_baja VARCHAR(255),
                        observaciones TEXT,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
            else:
                db.session.execute(text("""
                    CREATE TABLE bonificaciones_familiares (
                        id SERIAL PRIMARY KEY,
                        empleado_id INTEGER NOT NULL REFERENCES empleados(id) ON DELETE CASCADE,
                        hijo_nombre VARCHAR(120) NOT NULL,
                        hijo_apellido VARCHAR(120) NOT NULL,
                        hijo_ci VARCHAR(20),
                        hijo_fecha_nacimiento DATE NOT NULL,
                        sexo VARCHAR(1),
                        tipo tipohijoenum NOT NULL DEFAULT 'Menor de 18 años',
                        certificado_nacimiento VARCHAR(500),
                        certificado_estudio VARCHAR(500),
                        certificado_discapacidad VARCHAR(500),
                        activo BOOLEAN DEFAULT TRUE,
                        fecha_registro DATE DEFAULT CURRENT_DATE,
                        fecha_baja DATE,
                        motivo_baja VARCHAR(255),
                        observaciones TEXT,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
            db.session.commit()
            print("   ✅ Tabla 'bonificaciones_familiares' creada")
            
            # 5. AGREGAR columna a liquidaciones
            print("\n[5/6] Agregando columna 'bonificacion_familiar' a liquidaciones...")
            if es_sqlite:
                db.session.execute(text("""
                    ALTER TABLE liquidaciones 
                    ADD COLUMN bonificacion_familiar DECIMAL(12, 2) DEFAULT 0
                """))
            else:
                db.session.execute(text("""
                    ALTER TABLE liquidaciones 
                    ADD COLUMN bonificacion_familiar NUMERIC(12, 2) DEFAULT 0
                """))
            db.session.commit()
            print("   ✅ Columna 'bonificacion_familiar' agregada")
            
            # 6. INSERTAR salario mínimo 2025
            print("\n[6/6] Insertando salario mínimo vigente 2025...")
            db.session.execute(text("""
                INSERT INTO salarios_minimos (año, monto, vigencia_desde, vigencia_hasta)
                VALUES (2025, 2798309, '2025-01-01', NULL)
            """))
            db.session.commit()
            print("   ✅ Salario mínimo 2025: ₲ 2.798.309 Gs.")
            
            print("\n" + "=" * 60)
            print("✅ RECREACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 60)
            print("\nResumen:")
            print("  ✅ Tablas antiguas eliminadas")
            print("  ✅ Tabla 'salarios_minimos' creada")
            print("  ✅ ENUM 'tipohijoenum' creado")
            print("  ✅ Tabla 'bonificaciones_familiares' creada con todas las columnas")
            print("  ✅ Campo 'bonificacion_familiar' agregado a liquidaciones")
            print("  ✅ Salario mínimo 2025 registrado")
            print("\n📌 Próximos pasos:")
            print("  1. Reiniciar la aplicación: Ctrl+C y luego python run.py")
            print("  2. Acceder a: Menú → Nómina → Salarios Mínimos")
            print("  3. Registrar hijos: Menú → Empleados → [Empleado] → Pestaña Hijos")
            print("=" * 60)
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR durante la recreación: {str(e)}")
            print(f"Detalles: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    exito = recrear_tablas()
    sys.exit(0 if exito else 1)
