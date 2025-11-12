"""Añade columnas nuevas en la tabla `descuentos` (activo, origen_tipo, origen_id).

Uso (PowerShell):
 > python migrations\add_descuento_columns.py

El script detecta SQLite/Postgres y crea columnas si no existen.
"""
import sys
import os
from sqlalchemy import create_engine, text, inspect

# Añadir raíz al path por si acaso
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.models import db


def main():
    app = create_app()
    with app.app_context():
        engine = db.engine
        conn = engine.raw_connection()
        cursor = conn.cursor()
        db_type = engine.dialect.name
        print(f'Base de datos: {db_type}')

        try:
            # comprobar columna activo
            if db_type == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='descuentos' AND column_name='activo'
                    )
                """)
                exists = cursor.fetchone()[0]
            else:
                cursor.execute("PRAGMA table_info(descuentos)")
                exists = any(row[1] == 'activo' for row in cursor.fetchall())

            if not exists:
                print('Añadiendo descuentos.activo ...')
                if db_type == 'postgresql':
                    cursor.execute("ALTER TABLE descuentos ADD COLUMN activo BOOLEAN DEFAULT true")
                else:
                    cursor.execute("ALTER TABLE descuentos ADD COLUMN activo BOOLEAN DEFAULT 1")
                print('  ✓ agregado')
            else:
                print('✓ descuentos.activo ya existe')

            # comprobar origen_tipo
            if db_type == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='descuentos' AND column_name='origen_tipo'
                    )
                """)
                exists = cursor.fetchone()[0]
            else:
                cursor.execute("PRAGMA table_info(descuentos)")
                exists = any(row[1] == 'origen_tipo' for row in cursor.fetchall())

            if not exists:
                print('Añadiendo descuentos.origen_tipo ...')
                cursor.execute("ALTER TABLE descuentos ADD COLUMN origen_tipo VARCHAR(50)")
                print('  ✓ agregado')
            else:
                print('✓ descuentos.origen_tipo ya existe')

            # comprobar origen_id
            if db_type == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='descuentos' AND column_name='origen_id'
                    )
                """)
                exists = cursor.fetchone()[0]
            else:
                cursor.execute("PRAGMA table_info(descuentos)")
                exists = any(row[1] == 'origen_id' for row in cursor.fetchall())

            if not exists:
                print('Añadiendo descuentos.origen_id ...')
                cursor.execute("ALTER TABLE descuentos ADD COLUMN origen_id INTEGER")
                print('  ✓ agregado')
            else:
                print('✓ descuentos.origen_id ya existe')

            conn.commit()
            print('\n✓ Migración completada')
        except Exception as e:
            conn.rollback()
            print(f'Error durante migración: {e}')
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    main()
