#!/usr/bin/env python3
"""
migrate_add_empleado_fields.py
Script sencillo y práctico para añadir columnas esenciales a la tabla `empleados` en PostgreSQL.
Características:
 - Comprueba si la(s) columna(s) ya existen y añade solo las que falten (idempotente).
 - Opcional: crea un backup rápido (tabla copia) antes de aplicar cambios.
 - Ejecuta los ALTER TABLE dentro de una transacción.
 - Uso sencillo desde PowerShell.

Ejemplo:
  python scripts\migrate_add_empleado_fields.py --host localhost --port 5432 --dbname mydb --user myuser --backup

Dependencias:
  pip install psycopg2-binary

"""

import argparse
import os
import sys
import datetime
import getpass

try:
    import psycopg2
    from psycopg2 import sql
except Exception:
    print('Error: falta psycopg2. Instalar con: pip install psycopg2-binary')
    raise

COLUMNS = [
    ("nacionalidad", "VARCHAR(100)", "DEFAULT 'Paraguay'"),
    ("ips_numero", "VARCHAR(50)", None),
    ("motivo_retiro", "VARCHAR(255)", None),
]

TABLE_NAME = 'empleados'


def parse_args():
    p = argparse.ArgumentParser(description='Migración: añadir columnas esenciales a tabla empleados (Postgres)')
    p.add_argument('--host', default=os.environ.get('PGHOST', 'localhost'))
    p.add_argument('--port', type=int, default=int(os.environ.get('PGPORT', 5432)))
    p.add_argument('--dbname', default=os.environ.get('PGDATABASE'))
    p.add_argument('--user', default=os.environ.get('PGUSER'))
    p.add_argument('--password', default=os.environ.get('PGPASSWORD'))
    p.add_argument('--backup', action='store_true', help='Crear backup rápido (tabla copia) antes de migrar')
    p.add_argument('--yes', '-y', action='store_true', help='No pedir confirmación')
    return p.parse_args()


def confirm(prompt="¿Continuar? [y/N]: "):
    try:
        r = input(prompt).strip().lower()
        return r in ('y','yes')
    except KeyboardInterrupt:
        return False


def column_exists(cur, table, column):
    cur.execute(
        "SELECT 1 FROM information_schema.columns WHERE table_name=%s AND column_name=%s",
        (table, column)
    )
    return cur.fetchone() is not None


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
        try:
            password = getpass.getpass(f'Password for {args.user}@{args.host}: ')
        except Exception:
            password = None

    print('Resumen de migración:')
    print(f'  Host: {args.host}:{args.port}')
    print(f'  Database: {args.dbname}')
    print(f'  User: {args.user}')
    print(f'  Tabla: {TABLE_NAME}')
    print('  Columnas a comprobar: ' + ', '.join([c[0] for c in COLUMNS]))
    print(f'  Backup antes de migrar: {"Sí" if args.backup else "No"}')

    if not args.yes and not confirm():
        print('Cancelado por el usuario')
        sys.exit(0)

    conn = None
    def connect_with_fallback():
        # Intentar conexión normal; si falla por problemas de decodificación,
        # reintentar forzando client_encoding a LATIN1 (iso-8859-1 / cp1252 compatible).
        try:
            conn_local = psycopg2.connect(host=args.host, port=args.port, dbname=args.dbname, user=args.user, password=password)
            return conn_local
        except Exception as e:
            msg = str(e).lower()
            if 'codec' in msg or 'utf-8' in msg or 'decode' in msg or isinstance(e, UnicodeDecodeError):
                print('Advertencia: se detectó un error de decodificación al conectar. Reintentando con client_encoding=LATIN1')
                try:
                    conn_local = psycopg2.connect(host=args.host, port=args.port, dbname=args.dbname, user=args.user, password=password, options='-c client_encoding=LATIN1')
                    return conn_local
                except Exception as e2:
                    print('Reintento con LATIN1 falló:', e2)
                    raise
            else:
                raise

    try:
        conn = connect_with_fallback()
        cur = conn.cursor()

        # Backup opcional
        if args.backup:
            ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_table = f"{TABLE_NAME}_backup_{ts}"
            print(f'Creando backup rápido en tabla: {backup_table} ...')
            cur.execute(sql.SQL("CREATE TABLE {} AS TABLE {};").format(sql.Identifier(backup_table), sql.Identifier(TABLE_NAME)))
            conn.commit()
            print('Backup creado.')

        to_add = []
        for col_name, col_type, col_default in COLUMNS:
            if column_exists(cur, TABLE_NAME, col_name):
                print(f'  - Columna ya existe: {col_name} (se omite)')
            else:
                to_add.append((col_name, col_type, col_default))

        if not to_add:
            print('No hay columnas nuevas para añadir. Nada que hacer.')
            return

        # Ejecutar los ALTER dentro de una transacción
        print('Añadiendo columnas faltantes...')
        try:
            for col_name, col_type, col_default in to_add:
                parts = [sql.SQL('ALTER TABLE'), sql.Identifier(TABLE_NAME), sql.SQL('ADD COLUMN'), sql.Identifier(col_name), sql.SQL(col_type)]
                if col_default:
                    parts.append(sql.SQL(col_default))
                stmt = sql.SQL(' ').join(parts) + sql.SQL(';')
                cur.execute(stmt)
                print(f'  - Añadida columna: {col_name}')

            # Opcional: si añadimos nacionalidad con DEFAULT, setear NULLs existentes
            if any(c[0] == 'nacionalidad' for c in to_add):
                print("Asegurando valores de 'nacionalidad' para filas existentes (si NULL -> 'Paraguay')...")
                cur.execute(sql.SQL("UPDATE {} SET nacionalidad = 'Paraguay' WHERE nacionalidad IS NULL;").format(sql.Identifier(TABLE_NAME)))

            conn.commit()
            print('Migración completada y commit realizado.')

        except Exception as e:
            conn.rollback()
            print('Error al aplicar cambios, se hizo rollback. Error:', e)
            sys.exit(1)

    except Exception as e:
        # Si hay un error relacionado con decodificación/encoding, intentar usar psql como fallback
        msg = str(e).lower()
        need_psql = False
        if 'codec' in msg or 'utf-8' in msg or 'decode' in msg or isinstance(e, UnicodeDecodeError):
            need_psql = True

        if need_psql:
            print('Fallo en psycopg2 debido a problemas de encoding. Intentando fallback usando psql -f ...')
            try:
                import subprocess
                sql_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'add_empleado_fields.sql')
                if not os.path.exists(sql_file):
                    print('No se encontró el archivo SQL para fallback en:', sql_file)
                    sys.exit(1)

                cmd = [
                    'psql',
                    '-h', str(args.host),
                    '-p', str(args.port),
                    '-U', str(args.user),
                    '-d', str(args.dbname),
                    '-f', sql_file
                ]

                env = os.environ.copy()
                if password:
                    env['PGPASSWORD'] = password
                print('Ejecutando:', ' '.join(cmd))
                completed = subprocess.run(cmd, env=env)
                if completed.returncode != 0:
                    print('psql devolvió código', completed.returncode)
                    sys.exit(completed.returncode)
                print('Fallback con psql completado correctamente.')
                sys.exit(0)
            except FileNotFoundError:
                print('psql no se encontró en PATH. Instala psql o corrige la conexión.')
                sys.exit(1)
            except Exception as e2:
                print('Fallback con psql falló:', e2)
                sys.exit(1)

        print('Error de conexión o ejecución:', e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
