"""Script para migrar TODOS los nuevos modelos a PostgreSQL.

Crea:
1. Columna justificativo_archivo en sanciones
2. Tabla detalles_liquidacion (DetalleLiquidacion)
3. Tabla familiares_empleados (FamiliarEmpleado)
4. Tabla bonificaciones_familiares (BonificacionFamiliar)
5. Tabla postulantes (Postulante)
6. Tabla documentos_curriculum (DocumentosCurriculum)

Fuerza conexión a PostgreSQL usando DATABASE_URL de .env

Ejecución (PowerShell):
 > python migrations\add_new_models_pg.py
"""
import os
import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse

def parse_database_url(database_url):
    """Parsea DATABASE_URL postgresql://user:pass@host:port/dbname"""
    parsed = urlparse(database_url)
    return {
        'user': parsed.username,
        'password': parsed.password or '',
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'database': parsed.path.lstrip('/') or 'rrhh_db'
    }

def main():
    # Cargar .env si existe
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    # Obtener DATABASE_URL
    database_url = os.environ.get('DATABASE_URL', '')
    
    if not database_url or not database_url.startswith('postgresql://'):
        print('❌ DATABASE_URL no está configurada o es inválida en .env')
        print('   Asegúrate de tener en .env:')
        print('   DATABASE_URL=postgresql://user:password@host:5432/dbname')
        return
    
    # Parsear DATABASE_URL
    db_config = parse_database_url(database_url)
    
    print(f'🔌 Conectando a PostgreSQL: {db_config["user"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}')

    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()

        # ===== 1. Añadir columna justificativo_archivo en sanciones =====
        print('\n📋 [1/6] Verificando columna sanciones.justificativo_archivo...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='sanciones' AND column_name='justificativo_archivo'
            )
        """)
        col_exists = cursor.fetchone()[0]

        if not col_exists:
            print('  → Añadiendo columna justificativo_archivo a sanciones...')
            cursor.execute('ALTER TABLE sanciones ADD COLUMN justificativo_archivo VARCHAR(255)')
            conn.commit()
            print('  ✓ Columna justificativo_archivo en sanciones añadida')
        else:
            print('  ✓ Columna justificativo_archivo en sanciones ya existe')

        # ===== 2. Crear tabla detalles_liquidacion =====
        print('\n💾 [2/6] Verificando tabla detalles_liquidacion...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='detalles_liquidacion'
            )
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print('  → Creando tabla detalles_liquidacion...')
            cursor.execute("""
                CREATE TABLE detalles_liquidacion (
                    id SERIAL PRIMARY KEY,
                    liquidacion_id INTEGER NOT NULL REFERENCES liquidaciones(id) ON DELETE CASCADE,
                    tipo_rubro VARCHAR(50) NOT NULL,
                    descripcion VARCHAR(255) NOT NULL,
                    monto NUMERIC(12, 2) NOT NULL,
                    porcentaje NUMERIC(5, 3) DEFAULT 0,
                    UNIQUE(liquidacion_id, tipo_rubro, descripcion)
                )
            """)
            conn.commit()
            print('  ✓ Tabla detalles_liquidacion creada')
        else:
            print('  ✓ Tabla detalles_liquidacion ya existe')

        # ===== 3. Crear tabla familiares_empleados =====
        print('\n👨‍👩‍👧 [3/6] Verificando tabla familiares_empleados...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='familiares_empleados'
            )
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print('  → Creando tabla familiares_empleados...')
            cursor.execute("""
                CREATE TABLE familiares_empleados (
                    id SERIAL PRIMARY KEY,
                    empleado_id INTEGER NOT NULL REFERENCES empleados(id) ON DELETE CASCADE,
                    nombre VARCHAR(120) NOT NULL,
                    tipo VARCHAR(50) NOT NULL,
                    fecha_nacimiento DATE,
                    ci VARCHAR(20),
                    activo BOOLEAN DEFAULT TRUE,
                    fecha_inicio DATE DEFAULT CURRENT_DATE,
                    fecha_fin DATE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print('  ✓ Tabla familiares_empleados creada')
        else:
            print('  ✓ Tabla familiares_empleados ya existe')

        # ===== 4. Crear tabla bonificaciones_familiares =====
        print('\n💰 [4/6] Verificando tabla bonificaciones_familiares...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='bonificaciones_familiares'
            )
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print('  → Creando tabla bonificaciones_familiares...')
            cursor.execute("""
                CREATE TABLE bonificaciones_familiares (
                    id SERIAL PRIMARY KEY,
                    liquidacion_id INTEGER NOT NULL REFERENCES liquidaciones(id) ON DELETE CASCADE,
                    empleado_id INTEGER NOT NULL REFERENCES empleados(id) ON DELETE CASCADE,
                    familiar_id INTEGER NOT NULL REFERENCES familiares_empleados(id) ON DELETE CASCADE,
                    monto_unitario NUMERIC(12, 2) NOT NULL,
                    mes INTEGER,
                    año INTEGER,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print('  ✓ Tabla bonificaciones_familiares creada')
        else:
            print('  ✓ Tabla bonificaciones_familiares ya existe')

        # ===== 5. Crear tabla postulantes =====
        print('\n🎯 [5/6] Verificando tabla postulantes...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='postulantes'
            )
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print('  → Creando tabla postulantes...')
            cursor.execute("""
                CREATE TABLE postulantes (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(120) NOT NULL,
                    apellido VARCHAR(120) NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    telefono VARCHAR(20),
                    cargo_postulado VARCHAR(120) NOT NULL,
                    experiencia_años INTEGER DEFAULT 0,
                    salario_esperado NUMERIC(12, 2),
                    fecha_postulacion DATE DEFAULT CURRENT_DATE,
                    estado VARCHAR(50) DEFAULT 'Nuevo',
                    observaciones TEXT,
                    empleado_id INTEGER REFERENCES empleados(id),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print('  ✓ Tabla postulantes creada')
        else:
            print('  ✓ Tabla postulantes ya existe')

        # ===== 6. Crear tabla documentos_curriculum =====
        print('\n📄 [6/6] Verificando tabla documentos_curriculum...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='documentos_curriculum'
            )
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print('  → Creando tabla documentos_curriculum...')
            cursor.execute("""
                CREATE TABLE documentos_curriculum (
                    id SERIAL PRIMARY KEY,
                    postulante_id INTEGER NOT NULL REFERENCES postulantes(id) ON DELETE CASCADE,
                    tipo VARCHAR(50) NOT NULL,
                    nombre_archivo VARCHAR(255) NOT NULL,
                    ruta_archivo VARCHAR(500) NOT NULL,
                    tamaño_bytes INTEGER,
                    mime_type VARCHAR(100),
                    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print('  ✓ Tabla documentos_curriculum creada')
        else:
            print('  ✓ Tabla documentos_curriculum ya existe')

        cursor.close()
        conn.close()

        print('\n' + '='*60)
        print('✅ ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!')
        print('='*60)
        print('\nTablas y columnas creadas/verificadas:')
        print('  1. ✓ sanciones.justificativo_archivo')
        print('  2. ✓ detalles_liquidacion')
        print('  3. ✓ familiares_empleados')
        print('  4. ✓ bonificaciones_familiares')
        print('  5. ✓ postulantes')
        print('  6. ✓ documentos_curriculum')
        print('\n🔄 Ahora reinicia la aplicación Flask para que cargue los cambios.')
        print('   Ejecuta: python run.py')

    except psycopg2.Error as e:
        print(f'\n❌ Error de PostgreSQL: {e}')
        print(f'Código: {e.pgcode}')
        raise
    except Exception as e:
        print(f'\n❌ Error: {e}')
        raise

if __name__ == '__main__':
    main()
