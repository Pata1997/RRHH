"""
Migración: Crea tabla 'despidos' y añade columnas a 'liquidaciones'.
Compatible con SQLite y PostgreSQL.
"""
import sqlite3
import os

def try_postgres():
    """Intenta conectar a PostgreSQL, retorna conexión o None."""
    try:
        import psycopg2
        
        pg_host = os.environ.get('PGHOST', 'localhost')
        pg_port = os.environ.get('PGPORT', '5432')
        pg_user = os.environ.get('PGUSER', 'rrhh')
        pg_password = os.environ.get('PGPASSWORD', 'rrhh')
        pg_database = os.environ.get('PGDATABASE', 'rrhh')
        
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_password,
            database=pg_database,
            connect_timeout=5
        )
        return conn, 'postgres'
    except:
        return None, None

def main():
    print("=" * 70)
    print("MIGRACIÓN: Añadiendo tabla despidos y campos en liquidaciones")
    print("=" * 70)
    
    # Intentar PostgreSQL primero
    conn, dialect = try_postgres()
    
    if not conn:
        # Fallback a SQLite
        db_path = 'instance/rrhh.db'
        if not os.path.exists(db_path):
            print(f"\n⚠ Base de datos SQLite no encontrada en {db_path}")
            return
        
        try:
            conn = sqlite3.connect(db_path)
            dialect = 'sqlite'
            print(f"\n✓ Conectado a SQLite: {db_path}\n")
        except Exception as sqlite_err:
            print(f"\n✗ Error con SQLite: {sqlite_err}")
            return
    else:
        print(f"\n✓ Conectado a PostgreSQL\n")
    
    cursor = conn.cursor()
    
    try:
        print(f"Base de datos detectada: {dialect.upper()}\n")
        
        # === CREAR TABLA DESPIDOS ===
        print("1. Creando tabla 'despidos'...")
        
        if dialect == 'sqlite':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS despidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleado_id INTEGER NOT NULL,
                    tipo VARCHAR(50) NOT NULL,
                    causal VARCHAR(100),
                    descripcion TEXT,
                    fecha_despido DATE NOT NULL,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usuario_id INTEGER,
                    FOREIGN KEY(empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                )
            """)
        else:  # postgres
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS despidos (
                    id SERIAL PRIMARY KEY,
                    empleado_id INTEGER NOT NULL,
                    tipo VARCHAR(50) NOT NULL,
                    causal VARCHAR(100),
                    descripcion TEXT,
                    fecha_despido DATE NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario_id INTEGER,
                    FOREIGN KEY(empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                )
            """)
        
        print("   ✓ Tabla 'despidos' creada exitosamente")
        
        # === AÑADIR COLUMNAS A LIQUIDACIONES ===
        print("\n2. Verificando y añadiendo columnas en 'liquidaciones'...\n")
        
        nuevas_cols = {
            'despido_id': ('INTEGER', None),
            'indemnizacion_monto': ('NUMERIC(12,2)', 'DEFAULT 0'),
            'aguinaldo_monto': ('NUMERIC(12,2)', 'DEFAULT 0'),
            'vacaciones_monto': ('NUMERIC(12,2)', 'DEFAULT 0'),
            'aportes_ips_despido': ('NUMERIC(12,2)', 'DEFAULT 0'),
        }
        
        if dialect == 'sqlite':
            # Obtener columnas existentes
            cursor.execute("PRAGMA table_info(liquidaciones)")
            cols_existentes = {row[1] for row in cursor.fetchall()}
            
            for col_name, (col_type, default_clause) in nuevas_cols.items():
                if col_name not in cols_existentes:
                    sql = f"ALTER TABLE liquidaciones ADD COLUMN {col_name} {col_type}"
                    if default_clause:
                        sql += f" {default_clause}"
                    cursor.execute(sql)
                    print(f"   ✓ Columna 'liquidaciones.{col_name}' agregada")
                else:
                    print(f"   • Columna 'liquidaciones.{col_name}' ya existe")
        
        else:  # postgres
            import psycopg2.errors
            
            # Obtener columnas existentes
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='liquidaciones'
            """)
            cols_existentes = {row[0] for row in cursor.fetchall()}
            
            for col_name, (col_type, default_clause) in nuevas_cols.items():
                if col_name not in cols_existentes:
                    sql = f"ALTER TABLE liquidaciones ADD COLUMN {col_name} {col_type}"
                    if default_clause:
                        sql += f" {default_clause}"
                    try:
                        cursor.execute(sql)
                        print(f"   ✓ Columna 'liquidaciones.{col_name}' agregada")
                    except psycopg2.errors.DuplicateColumn:
                        print(f"   • Columna 'liquidaciones.{col_name}' ya existe")
                else:
                    print(f"   • Columna 'liquidaciones.{col_name}' ya existe")
        
        # === CREAR FK EN LIQUIDACIONES (si no existe) ===
        print("\n3. Verificando relación entre despidos y liquidaciones...")
        
        if dialect == 'sqlite':
            print("   • SQLite: Relación FK validada en modelo")
        else:
            import psycopg2.errors
            try:
                constraint_query = """
                    SELECT constraint_name FROM information_schema.table_constraints
                    WHERE table_name='liquidaciones' AND constraint_name='fk_liquidaciones_despido_id'
                """
                cursor.execute(constraint_query)
                exists = cursor.fetchone()
                
                if not exists:
                    cursor.execute("""
                        ALTER TABLE liquidaciones
                        ADD CONSTRAINT fk_liquidaciones_despido_id
                        FOREIGN KEY(despido_id) REFERENCES despidos(id) ON DELETE SET NULL
                    """)
                    print("   ✓ Foreign Key 'fk_liquidaciones_despido_id' agregada")
                else:
                    print("   • Foreign Key ya existe")
            except psycopg2.errors.DuplicateObject:
                print("   • Foreign Key ya existe")
            except Exception as fk_err:
                print(f"   ⚠ No se pudo agregar FK: {fk_err}")
        
        conn.commit()
        print("\n" + "=" * 70)
        print("✓ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERROR durante la migración: {e}")
        if conn:
            conn.rollback()
        import traceback
        traceback.print_exc()
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
