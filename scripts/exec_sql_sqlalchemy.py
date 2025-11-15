#!/usr/bin/env python3
"""
exec_sql_sqlalchemy.py
Ejecuta un archivo SQL contra una base de datos usando SQLAlchemy.
Útil cuando `psql` no está disponible en PATH en Windows.

Uso:
  python scripts\exec_sql_sqlalchemy.py --host localhost --port 5432 --dbname mydb --user myuser --sql-file sql/add_empleado_fields_null.sql

También puede usarse pasando una URI completa con --db-uri.

"""
import argparse
import os
import sys
import getpass
from sqlalchemy import create_engine, text


def parse_args():
    p = argparse.ArgumentParser(description='Ejecuta un SQL file usando SQLAlchemy')
    p.add_argument('--db-uri', help='URI completa SQLAlchemy (ej: postgresql+psycopg2://user:pass@host:port/dbname)')
    p.add_argument('--host', default=os.environ.get('PGHOST', 'localhost'))
    p.add_argument('--port', default=os.environ.get('PGPORT', '5432'))
    p.add_argument('--dbname', default=os.environ.get('PGDATABASE'))
    p.add_argument('--user', default=os.environ.get('PGUSER'))
    p.add_argument('--password', default=os.environ.get('PGPASSWORD'))
    p.add_argument('--sql-file', default=os.path.join('sql', 'add_empleado_fields_null.sql'))
    return p.parse_args()


def read_sql_file(path):
    # Leer preferentemente con latin-1 para evitar problemas con archivos creados en Windows
    try:
        with open(path, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception:
        # Fallback a utf-8 si algo raro ocurre
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()


def build_uri_from_parts(user, password, host, port, dbname):
    if not user:
        raise ValueError('user requerido si no usas --db-uri')
    pwd_part = f":{password}" if password else ''
    return f"postgresql+psycopg2://{user}{pwd_part}@{host}:{port}/{dbname}"


def main():
    args = parse_args()

    sql_file = args.sql_file
    if not os.path.exists(sql_file):
        print('No se encontró el archivo SQL en:', os.path.abspath(sql_file))
        sys.exit(2)

    if args.db_uri:
        db_uri = args.db_uri
    else:
        if not args.dbname or not args.user:
            print('Si no pasás --db-uri, debés indicar --dbname y --user (o exportar PGDATABASE/PGUSER)')
            sys.exit(2)
        password = args.password
        if password is None:
            try:
                password = getpass.getpass(f'Password for {args.user}@{args.host}: ')
            except Exception:
                password = None
        db_uri = build_uri_from_parts(args.user, password, args.host, args.port, args.dbname)

    print('DB URI:', db_uri)
    print('SQL file:', os.path.abspath(sql_file))

    sql_text = read_sql_file(sql_file)

    # Forzar client encoding en la conexión creando engine con opciones para psycopg2
    connect_args = {}
    # si la URI es postgresql+psycopg2, intentar forzar options para client_encoding
    if 'postgresql+psycopg2' in db_uri:
        connect_args = {'options': "-c client_encoding=LATIN1"}
    engine = create_engine(db_uri, connect_args=connect_args)
    # Ejecutar en transacción
    try:
        with engine.begin() as conn:
            # Forzar client_encoding a LATIN1 en la sesión para evitar errores de decodificación
            try:
                conn.execute(text("SET client_encoding TO 'LATIN1';"))
            except Exception:
                # Si el SET falla, continuar de todas formas
                pass

            # Ejecutar todo el script dividiendo por ';' — suficiente para statements simples
            statements = [s.strip() for s in sql_text.split(';') if s.strip()]
            for st in statements:
                print('Ejecutando statement (primeros 120 chars):', st[:120].replace('\n', ' '))
                conn.execute(text(st))
        print('SQL ejecutado correctamente.')
    except Exception as e:
        import traceback
        print('Error al ejecutar SQL:')
        traceback.print_exc()
        # Mostrar posible detalle de encoding
        print('\nDetalle (str):', str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
