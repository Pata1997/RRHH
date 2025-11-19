"""
Script directo para PostgreSQL - Recrear Bonificación Familiar
Conecta directamente a PostgreSQL sin pasar por Flask
"""

import psycopg2
import sys

def recrear_tablas_postgres():
    """Recrear tablas directamente en PostgreSQL"""
    
    print("=" * 60)
    print("RECREACIÓN: Bonificación Familiar (PostgreSQL)")
    print("=" * 60)
    
    # Conexión a PostgreSQL
    connection_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'rrhh_db',
        'user': 'rrhh_user',
        'password': '123456'
    }
    
    conn = None
    try:
        print(f"\n🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()
        print("   ✅ Conexión establecida")
        
        # 1. ELIMINAR tablas existentes
        print("\n[1/6] Eliminando tablas existentes...")
        
        cursor.execute("DROP TABLE IF EXISTS bonificaciones_familiares CASCADE")
        print("   ✅ Tabla bonificaciones_familiares eliminada")
        
        cursor.execute("DROP TABLE IF EXISTS salarios_minimos CASCADE")
        print("   ✅ Tabla salarios_minimos eliminada")
        
        cursor.execute("DROP TYPE IF EXISTS tipohijoenum CASCADE")
        print("   ✅ ENUM tipohijoenum eliminado")
        
        # 2. CREAR tabla salarios_minimos
        print("\n[2/6] Creando tabla 'salarios_minimos'...")
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
        
        # 3. CREAR enum tipohijoenum
        print("\n[3/6] Creando ENUM 'tipohijoenum'...")
        cursor.execute("""
            CREATE TYPE tipohijoenum AS ENUM (
                'Menor de 18 años',
                'Mayor de 18 años - Estudiante',
                'Hijo con discapacidad'
            )
        """)
        print("   ✅ ENUM 'tipohijoenum' creado")
        
        # 4. CREAR tabla bonificaciones_familiares
        print("\n[4/6] Creando tabla 'bonificaciones_familiares'...")
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
        
        # 5. AGREGAR columna a liquidaciones (si no existe)
        print("\n[5/6] Agregando columna 'bonificacion_familiar' a liquidaciones...")
        try:
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='liquidaciones' AND column_name='bonificacion_familiar'
            """)
            if cursor.fetchone():
                print("   ℹ️  Columna 'bonificacion_familiar' ya existe")
            else:
                cursor.execute("""
                    ALTER TABLE liquidaciones 
                    ADD COLUMN bonificacion_familiar NUMERIC(12, 2) DEFAULT 0
                """)
                print("   ✅ Columna 'bonificacion_familiar' agregada")
        except Exception as e:
            print(f"   ⚠️  Error con columna: {e}")
        
        # 6. INSERTAR salario mínimo 2025
        print("\n[6/6] Insertando salario mínimo vigente 2025...")
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
        print("✅ RECREACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nResumen:")
        print("  ✅ Tablas antiguas eliminadas")
        print("  ✅ Tabla 'salarios_minimos' creada")
        print("  ✅ ENUM 'tipohijoenum' creado")
        print("  ✅ Tabla 'bonificaciones_familiares' creada con columna 'activo'")
        print("  ✅ Campo 'bonificacion_familiar' agregado a liquidaciones")
        print("  ✅ Salario mínimo 2025 registrado")
        print("\n📌 Próximos pasos:")
        print("  1. Reiniciar aplicación: python run.py")
        print("  2. Acceder a: http://127.0.0.1:5000")
        print("  3. Ir a: Menú → Nómina → Salarios Mínimos")
        print("  4. Registrar hijos: Empleados → Ver → Pestaña Hijos")
        print("=" * 60)
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ ERROR de PostgreSQL: {e}")
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
    print("\n⚠️  ADVERTENCIA: Este script eliminará y recreará las tablas.")
    print("Si ya tienes datos de bonificaciones familiares, se perderán.")
    
    respuesta = input("\n¿Continuar? (si/no): ").lower().strip()
    
    if respuesta in ['si', 's', 'yes', 'y']:
        exito = recrear_tablas_postgres()
        sys.exit(0 if exito else 1)
    else:
        print("\n❌ Operación cancelada")
        sys.exit(1)
