#!/usr/bin/env python3
"""
scrp_actualizacion.py
Ejecuta el script SQL `sql/add_empleado_fields.sql` contra una base PostgreSQL.
Uso:
  python scripts/scrp_actualizacion.py --host localhost --port 5432 --dbname mi_db --user mi_usuario

El script intenta crear un backup rápido (opcional) y luego ejecutar el SQL dentro de una transacción.
Requiere: psycopg2 (recomendado: psycopg2-binary)
Instalación: pip install psycopg2-binary
"""

import argparse
import os
import sys
import datetime
import getpass

try:
    import psycopg2
    from psycopg2 import sql
except Exception as e:
    print("Error: no se pudo importar psycopg2. Instala con: pip install psycopg2-binary")
    raise

DEFAULT_SQL = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'add_empleado_fields.sql')


def parse_args():
    p = argparse.ArgumentParser(description='Ejecuta SQL para añadir columnas a empleados (Postgres)')
    p.add_argument('--host', default=os.environ.get('PGHOST', 'localhost'))
    p.add_argument('--port', type=int, default=int(os.environ.get('PGPORT', 5432)))
    p.add_argument('--dbname', default=os.environ.get('PGDATABASE'))
    p.add_argument('--user', default=os.environ.get('PGUSER'))
    p.add_argument('--password', default=os.environ.get('PGPASSWORD'))
    p.add_argument('--sql-file', default=DEFAULT_SQL)
    p.add_argument('--backup', action='store_true', help='Crear backup rápido: copia tabla empleados a empleados_backup_YYYYMMDD_HHMMSS')
    p.add_argument('--yes', '-y', action='store_true', help='No preguntar confirmación')
    return p.parse_args()


def confirm(prompt="¿Continuar? [y/N]: "):
    try:
        r = input(prompt).strip().lower()
        return r in ('y','yes')
    except KeyboardInterrupt:
        return False


def main():
    args = parse_args()

    if not args.dbname:
        print('Error: indica --dbname o exporta PGDATABASE en el entorno')
        sys.exit(2)
    if not args.user:
        print('Error: indica --user o exporta PGUSER en el entorno')
        sys.exit(2)

    password = args.password
    if password is None:
        # No forzamos mostrar password en consola si ya hay variable
        try:
            password = getpass.getpass(f'Password for {args.user}@{args.host}: ')
        except Exception:
            password = None

    if not os.path.exists(args.sql_file):
        print(f"Error: no existe el archivo SQL: {args.sql_file}")
        sys.exit(2)

    print("Resumen:")
    print(f"  Host: {args.host}:{args.port}")
    print(f"  Database: {args.dbname}")
    print(f"  User: {args.user}")
    print(f"  SQL file: {args.sql_file}")
    print(f"  Backup: {'Sí' if args.backup else 'No'}")

    if not args.yes and not confirm():
        print('Cancelado por el usuario')
        sys.exit(0)

    conn = None
    try:
        conn = psycopg2.connect(host=args.host, port=args.port, dbname=args.dbname, user=args.user, password=password)
        conn.autocommit = False
        cur = conn.cursor()

        if args.backup:
            ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_table = f"empleados_backup_{ts}"
            print(f"Creando backup rápido en tabla: {backup_table} ...")
            cur.execute(sql.SQL("CREATE TABLE {} AS TABLE empleados").format(sql.Identifier(backup_table)))
            print("Backup creado.")

        # Leer SQL: intentar utf-8, si falla reintentar con latin-1 (cp1252)
        sql_text = None
        try:
            with open(args.sql_file, 'r', encoding='utf-8') as f:
                sql_text = f.read()
            print('Leído SQL usando encoding utf-8')
        except UnicodeDecodeError:
            print('Advertencia: fallo en decodificar con utf-8, reintentando con latin-1')
            with open(args.sql_file, 'r', encoding='latin-1') as f:
                sql_text = f.read()
            print('Leído SQL usando encoding latin-1')

        print('Ejecutando SQL...')
        cur.execute(sql_text)
        conn.commit()
        print('SQL ejecutado y commit realizado.')

        # ANALYZE
        print('Actualizando estadísticas (ANALYZE empleados) ...')
        cur.execute('ANALYZE empleados;')
        conn.commit()
        print('Hecho.')

        cur.close()
        print('Operación finalizada con éxito.')

    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        print('Error durante la operación:', e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
