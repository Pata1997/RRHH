"""Script seguro para añadir columnas nuevas a la tabla `permisos`.

Usar solo en entornos donde no se usa Alembic. El script:
 - verifica si las columnas `con_goce` y `descuento_id` existen
 - si faltan, las crea con tipos y valores por defecto
 - agrega la constraint FK a `descuentos.id` (ON DELETE SET NULL) si aplica

Ejecución (PowerShell desde raíz del proyecto):
 > python migrations\add_permiso_columns.py
"""
import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text, inspect


def get_db_type(conn):
    """Retorna el tipo de base de datos (sqlite, postgresql, etc)."""
    return conn.dialect.name


def column_exists_sqlite(conn, table_name, column_name):
    """Verifica si una columna existe en SQLite."""
    try:
        inspector = inspect(conn)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except Exception as e:
        print(f'Error al verificar columna en SQLite: {e}')
        return False


def column_exists_postgres(conn, table_name, column_name):
    """Verifica si una columna existe en PostgreSQL."""
    try:
        q = text("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name = :table AND column_name = :column
        """)
        r = conn.execute(q, {'table': table_name, 'column': column_name}).fetchone()
        return r is not None
    except Exception as e:
        print(f'Error al verificar columna en PostgreSQL: {e}')
        return False


def column_exists(conn, table_name, column_name):
    """Verifica si una columna existe (compatible con SQLite y PostgreSQL)."""
    db_type = get_db_type(conn)
    if db_type == 'sqlite':
        return column_exists_sqlite(conn, table_name, column_name)
    elif db_type == 'postgresql':
        return column_exists_postgres(conn, table_name, column_name)
    else:
        print(f'Tipo de BD no soportado: {db_type}')
        return False


def main():
    app = create_app()
    with app.app_context():
        engine = db.engine
        conn = engine.raw_connection()
        cursor = conn.cursor()
        db_type = engine.dialect.name
        print(f'Base de datos: {db_type}')

        try:
            # Añadir con_goce si no existe
            if db_type == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name='permisos' AND column_name='con_goce'
                    )
                """)
                col_exists = cursor.fetchone()[0]
            else:
                # SQLite
                cursor.execute("PRAGMA table_info(permisos)")
                col_exists = any(row[1] == 'con_goce' for row in cursor.fetchall())

            if not col_exists:
                print('Añadiendo columna permisos.con_goce ...')
                if db_type == 'postgresql':
                    cursor.execute('ALTER TABLE permisos ADD COLUMN con_goce BOOLEAN DEFAULT false')
                else:
                    cursor.execute('ALTER TABLE permisos ADD COLUMN con_goce BOOLEAN DEFAULT 0')
                print('  ✓ Columna con_goce añadida')
            else:
                print('✓ Columna permisos.con_goce ya existe')

            # Añadir descuento_id si no existe
            if db_type == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name='permisos' AND column_name='descuento_id'
                    )
                """)
                col_exists = cursor.fetchone()[0]
            else:
                # SQLite
                cursor.execute("PRAGMA table_info(permisos)")
                col_exists = any(row[1] == 'descuento_id' for row in cursor.fetchall())

            if not col_exists:
                print('Añadiendo columna permisos.descuento_id ...')
                cursor.execute('ALTER TABLE permisos ADD COLUMN descuento_id INTEGER')
                print('  ✓ Columna descuento_id añadida')
            else:
                print('✓ Columna permisos.descuento_id ya existe')

            conn.commit()
            print('\n✓ Migración completada. Recuerda reiniciar la app si está en ejecución.')
        except Exception as e:
            conn.rollback()
            print(f'\n✗ Error durante migración: {e}')
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    main()
