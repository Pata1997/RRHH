"""Script para añadir columnas a la tabla `permisos` en PostgreSQL.

Fuerza conexión a PostgreSQL usando variables de entorno.

Ejecución (PowerShell):
 > python migrations\add_permiso_columns_pg.py
"""
import os
import psycopg2
from psycopg2 import sql

def main():
    # Obtener credenciales de variables de entorno o usar defaults
    host = os.environ.get('PGHOST', 'localhost')
    port = os.environ.get('PGPORT', '5432')
    user = os.environ.get('PGUSER', 'postgres')
    password = os.environ.get('PGPASSWORD', '')
    database = os.environ.get('PGDATABASE', 'rrhh_db')

    print(f'Conectando a PostgreSQL: {user}@{host}:{port}/{database}')

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Verificar y añadir columna con_goce
        print('\nVerificando columna permisos.con_goce...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='permisos' AND column_name='con_goce'
            )
        """)
        con_goce_exists = cursor.fetchone()[0]

        if not con_goce_exists:
            print('  → Añadiendo columna con_goce...')
            cursor.execute('ALTER TABLE permisos ADD COLUMN con_goce BOOLEAN DEFAULT false')
            conn.commit()
            print('  ✓ Columna con_goce añadida exitosamente')
        else:
            print('  ✓ Columna con_goce ya existe')

        # Verificar y añadir columna descuento_id
        print('\nVerificando columna permisos.descuento_id...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='permisos' AND column_name='descuento_id'
            )
        """)
        descuento_id_exists = cursor.fetchone()[0]

        if not descuento_id_exists:
            print('  → Añadiendo columna descuento_id...')
            cursor.execute('ALTER TABLE permisos ADD COLUMN descuento_id INTEGER')
            conn.commit()
            print('  ✓ Columna descuento_id añadida exitosamente')
        else:
            print('  ✓ Columna descuento_id ya existe')

        # Intentar añadir FK (si no existe)
        print('\nVerificando Foreign Key...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.table_constraints
                WHERE table_name='permisos' AND constraint_name='fk_permisos_descuento'
            )
        """)
        fk_exists = cursor.fetchone()[0]

        if not fk_exists:
            print('  → Añadiendo constraint FK fk_permisos_descuento...')
            try:
                cursor.execute("""
                    ALTER TABLE permisos
                    ADD CONSTRAINT fk_permisos_descuento
                    FOREIGN KEY (descuento_id) REFERENCES descuentos(id) ON DELETE SET NULL
                """)
                conn.commit()
                print('  ✓ Constraint FK añadido exitosamente')
            except psycopg2.Error as e:
                if 'already exists' in str(e):
                    print('  ✓ Constraint FK ya existe')
                else:
                    print(f'  ⚠ Error al añadir FK (continuando): {e}')
                    conn.rollback()
        else:
            print('  ✓ Constraint FK ya existe')

        cursor.close()
        conn.close()

        print('\n' + '='*60)
        print('✓ Migración completada exitosamente')
        print('Recuerda reiniciar la app Flask si está en ejecución.')
        print('='*60)

    except psycopg2.OperationalError as e:
        print(f'\n✗ Error de conexión a PostgreSQL: {e}')
        print('\nVerifica:')
        print(f'  - PGHOST: {host}')
        print(f'  - PGPORT: {port}')
        print(f'  - PGUSER: {user}')
        print(f'  - PGDATABASE: {database}')
        print('\nConfigura variables de entorno si es necesario:')
        print('  $env:PGHOST = "localhost"')
        print('  $env:PGPORT = "5432"')
        print('  $env:PGUSER = "postgres"')
        print('  $env:PGPASSWORD = "tu_contraseña"')
        print('  $env:PGDATABASE = "rrhh_db"')
    except Exception as e:
        print(f'\n✗ Error inesperado: {e}')

if __name__ == '__main__':
    main()
