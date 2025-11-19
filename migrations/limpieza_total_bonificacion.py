"""
LIMPIEZA TOTAL Y VERIFICACIÓN - PostgreSQL
Elimina completamente las tablas y las recrea desde cero
"""

import psycopg2
import sys

def limpiar_todo():
    """Limpieza total de tablas de bonificación familiar"""
    
    print("=" * 70)
    print("LIMPIEZA TOTAL Y RECREACIÓN - Bonificación Familiar")
    print("=" * 70)
    
    conn = None
    try:
        # Conexión a PostgreSQL
        print(f"\n🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='rrhh_db',
            user='rrhh_user',
            password='123456'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("   ✅ Conexión establecida")
        
        # PASO 1: Verificar columnas actuales
        print("\n[DIAGNÓSTICO] Verificando estructura actual...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name='bonificaciones_familiares'
            ORDER BY ordinal_position
        """)
        columnas_actuales = cursor.fetchall()
        if columnas_actuales:
            print("   📋 Columnas encontradas:")
            for col in columnas_actuales:
                print(f"      - {col[0]} ({col[1]})")
        else:
            print("   ℹ️  Tabla no existe")
        
        # PASO 2: ELIMINAR TODO
        print("\n[1/5] Eliminando TODO...")
        
        # Eliminar vistas o dependencias si existen
        cursor.execute("DROP VIEW IF EXISTS vista_bonificaciones CASCADE")
        
        # Eliminar tabla bonificaciones_familiares con CASCADE
        cursor.execute("DROP TABLE IF EXISTS bonificaciones_familiares CASCADE")
        print("   ✅ Tabla bonificaciones_familiares ELIMINADA")
        
        # Eliminar tabla salarios_minimos
        cursor.execute("DROP TABLE IF EXISTS salarios_minimos CASCADE")
        print("   ✅ Tabla salarios_minimos ELIMINADA")
        
        # Eliminar ENUM
        cursor.execute("DROP TYPE IF EXISTS tipohijoenum CASCADE")
        print("   ✅ ENUM tipohijoenum ELIMINADO")
        
        # PASO 3: CREAR tabla salarios_minimos
        print("\n[2/5] Creando tabla 'salarios_minimos'...")
        cursor.execute("""
            CREATE TABLE salarios_minimos (
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
        
        # PASO 4: CREAR enum tipohijoenum
        print("\n[3/5] Creando ENUM 'tipohijoenum'...")
        cursor.execute("""
            CREATE TYPE tipohijoenum AS ENUM (
                'Menor de 18 años',
                'Mayor de 18 años - Estudiante',
                'Hijo con discapacidad'
            )
        """)
        print("   ✅ ENUM 'tipohijoenum' creado")
        
        # PASO 5: CREAR tabla bonificaciones_familiares (NUEVA Y LIMPIA)
        print("\n[4/5] Creando tabla 'bonificaciones_familiares' (nueva)...")
        cursor.execute("""
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
        """)
        print("   ✅ Tabla 'bonificaciones_familiares' creada")
        
        # PASO 6: Verificar columnas creadas
        print("\n[VERIFICACIÓN] Columnas creadas:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name='bonificaciones_familiares'
            ORDER BY ordinal_position
        """)
        columnas_nuevas = cursor.fetchall()
        for col in columnas_nuevas:
            print(f"   ✓ {col[0]:<30} {col[1]:<20} {'NULL' if col[2]=='YES' else 'NOT NULL'}")
        
        # PASO 7: Agregar columna a liquidaciones (si no existe)
        print("\n[5/5] Verificando columna en 'liquidaciones'...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='liquidaciones' AND column_name='bonificacion_familiar'
        """)
        if cursor.fetchone():
            print("   ✅ Columna 'bonificacion_familiar' ya existe")
        else:
            cursor.execute("""
                ALTER TABLE liquidaciones 
                ADD COLUMN bonificacion_familiar NUMERIC(12, 2) DEFAULT 0
            """)
            print("   ✅ Columna 'bonificacion_familiar' agregada")
        
        # PASO 8: Insertar salario mínimo 2025
        print("\n[6/6] Insertando salario mínimo 2025...")
        cursor.execute("SELECT COUNT(*) FROM salarios_minimos WHERE año = 2025")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO salarios_minimos (año, monto, vigencia_desde, vigencia_hasta)
                VALUES (2025, 2798309, '2025-01-01', NULL)
            """)
            print("   ✅ Salario mínimo 2025: ₲ 2.798.309")
        else:
            print("   ℹ️  Salario mínimo 2025 ya existe")
        
        print("\n" + "=" * 70)
        print("✅ LIMPIEZA Y RECREACIÓN COMPLETADA")
        print("=" * 70)
        print("\n📊 RESUMEN:")
        print("  ✅ Tablas viejas eliminadas completamente")
        print("  ✅ ENUM creado correctamente")
        print("  ✅ Tabla bonificaciones_familiares creada con 17 columnas correctas")
        print("  ✅ Tabla salarios_minimos creada")
        print("  ✅ Columna bonificacion_familiar en liquidaciones")
        print("  ✅ Salario mínimo 2025 registrado")
        print("\n⚠️  IMPORTANTE:")
        print("  1. CIERRA completamente todas las terminales de Python/Flask")
        print("  2. REINICIA el servidor: python run.py")
        print("  3. Los errores deben desaparecer completamente")
        print("=" * 70)
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ ERROR PostgreSQL: {e}")
        print(f"Código: {e.pgcode}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if conn:
            conn.close()
            print("\n🔌 Conexión cerrada")

if __name__ == '__main__':
    print("\n⚠️  Este script eliminará COMPLETAMENTE las tablas y las recreará.")
    print("Cualquier dato de bonificaciones existente se perderá.\n")
    
    respuesta = input("¿Confirmas la limpieza total? (escribe SI en mayúsculas): ").strip()
    
    if respuesta == 'SI':
        exito = limpiar_todo()
        sys.exit(0 if exito else 1)
    else:
        print("\n❌ Operación cancelada (debes escribir SI en mayúsculas)")
        sys.exit(1)
