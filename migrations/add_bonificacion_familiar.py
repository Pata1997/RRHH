"""
Migración: Agregar Bonificación Familiar
Fecha: 2025-11-19

Cambios:
1. Crear tabla salarios_minimos
2. Crear tabla bonificaciones_familiares (hijos de empleados)
3. Agregar campo bonificacion_familiar a liquidaciones
4. Insertar salario mínimo vigente actual
"""

import psycopg2
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def ejecutar_migracion():
    """Ejecuta la migración de bonificación familiar"""
    print("=" * 60)
    print("MIGRACIÓN: Bonificación Familiar")
    print("=" * 60)
    
    # Obtener configuración de base de datos desde variables de entorno
    db_url = os.getenv('DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI')
    
    if not db_url:
        print("\n❌ ERROR: No se encontró DATABASE_URL en las variables de entorno")
        print("Asegúrate de tener un archivo .env con DATABASE_URL configurado")
        return False
    
    # Parsear la URL de PostgreSQL
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', '', 1)
        # Formato: usuario:password@host:puerto/database
        auth_and_host = db_url.split('/')
        database = auth_and_host[1] if len(auth_and_host) > 1 else 'rrhh_db'
        
        user_pass_host = auth_and_host[0]
        if '@' in user_pass_host:
            auth, host_port = user_pass_host.split('@')
            user, password = auth.split(':') if ':' in auth else (auth, '')
            host, port = host_port.split(':') if ':' in host_port else (host_port, '5432')
        else:
            user = 'postgres'
            password = ''
            host = 'localhost'
            port = '5432'
    else:
        # Valores por defecto
        user = 'postgres'
        password = 'postgres'
        host = 'localhost'
        port = '5432'
        database = 'rrhh_db'
    
    conn = None
    try:
        # Conectar a PostgreSQL
        print(f"\n🔌 Conectando a PostgreSQL en {host}:{port}/{database}...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("   ✅ Conexión establecida")
        
        # 1. Crear tabla salarios_minimos
        print("\n[1/5] Creando tabla 'salarios_minimos'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salarios_minimos (
                id SERIAL PRIMARY KEY,
                año INTEGER NOT NULL,
                monto NUMERIC(12, 2) NOT NULL,
                vigencia_desde DATE NOT NULL,
                vigencia_hasta DATE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_creador_id INTEGER REFERENCES usuarios(id)
            )
        """)
        print("   ✅ Tabla 'salarios_minimos' creada")
        
        # 2. Crear enum tipo_hijo si no existe
        print("\n[2/5] Creando ENUM 'tipohijoenum'...")
        try:
            cursor.execute("""
                DO $$ BEGIN
                    CREATE TYPE tipohijoenum AS ENUM (
                        'Menor de 18 años',
                        'Mayor de 18 años - Estudiante',
                        'Hijo con discapacidad'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """)
            print("   ✅ ENUM 'tipohijoenum' creado")
        except Exception as e:
            print(f"   ℹ️  ENUM ya existe: {e}")
        
        # 3. Crear tabla bonificaciones_familiares
        print("\n[3/5] Creando tabla 'bonificaciones_familiares'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bonificaciones_familiares (
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
        """)
        print("   ✅ Tabla 'bonificaciones_familiares' creada")
        
        # 4. Agregar columna bonificacion_familiar a liquidaciones
        print("\n[4/5] Agregando columna 'bonificacion_familiar' a liquidaciones...")
        try:
            cursor.execute("""
                ALTER TABLE liquidaciones 
                ADD COLUMN IF NOT EXISTS bonificacion_familiar NUMERIC(12, 2) DEFAULT 0
            """)
            print("   ✅ Columna 'bonificacion_familiar' agregada")
        except Exception as e:
            print(f"   ℹ️  Columna ya existe: {e}")
        
        # 5. Insertar salario mínimo vigente actual (2025)
        print("\n[5/5] Insertando salario mínimo vigente 2025...")
        cursor.execute("SELECT COUNT(*) FROM salarios_minimos WHERE año = 2025")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("""
                INSERT INTO salarios_minimos (año, monto, vigencia_desde, vigencia_hasta)
                VALUES (2025, 2798309, '2025-01-01', NULL)
            """)
            print("   ✅ Salario mínimo 2025: ₲ 2.798.309 Gs.")
        else:
            cursor.execute("SELECT monto FROM salarios_minimos WHERE año = 2025")
            monto = cursor.fetchone()[0]
            print(f"   ℹ️  Salario mínimo 2025 ya existe: ₲ {float(monto):,.0f} Gs.")
        
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nResumen:")
        print("  ✅ Tabla 'salarios_minimos' creada")
        print("  ✅ Tabla 'bonificaciones_familiares' creada")
        print("  ✅ Campo 'bonificacion_familiar' agregado a liquidaciones")
        print("  ✅ Salario mínimo 2025 registrado")
        print("\n📌 Próximos pasos:")
        print("  1. Reiniciar la aplicación: python run.py")
        print("  2. Acceder a: Menú → Nómina → Salarios Mínimos")
        print("  3. Registrar hijos: Menú → Empleados → [Empleado] → Pestaña Hijos")
        print("  4. Las liquidaciones calcularán automáticamente la bonificación")
        print("=" * 60)
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ ERROR de PostgreSQL: {e}")
        print(f"Código: {e.pgcode}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR durante la migración: {str(e)}")
        print(f"Detalles: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if conn:
            conn.close()
            print("\n🔌 Conexión cerrada")

if __name__ == '__main__':
    exito = ejecutar_migracion()
    sys.exit(0 if exito else 1)
