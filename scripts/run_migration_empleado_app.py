#!/usr/bin/env python3
"""
run_migration_empleado_app.py

Carga la aplicación Flask (contexto) y ejecuta el script de migración
`scripts/migrate_add_empleado_fields.py` usando los datos de conexión
extraídos de `app.config['SQLALCHEMY_DATABASE_URI']`.

Comportamiento:
 - Importa `create_app` de `app` y carga config 'development'.
 - Extrae host/port/dbname/user/password si la URI es postgres.
 - Ejecuta el script de migración en un subprocess, pasando la conexión vía
   variables de entorno (PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD).
 - Ejecuta con `--backup` y `--yes` por defecto; puede pasarse `--no-backup`
   para omitir backup o `--no-yes` para requerir confirmación.

Uso:
  python scripts/run_migration_empleado_app.py [--no-backup] [--no-yes]

"""
import os
import sys
import subprocess
import argparse
from urllib.parse import urlparse
import sqlalchemy
from sqlalchemy import text

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Intentamos importar create_app desde app
try:
    from app import create_app
except Exception as e:
    print('Error: no se pudo importar create_app desde app:', e)
    print('Asegurate de ejecutar este script desde el directorio del proyecto o usa PYTHONPATH apuntando al proyecto.')
    raise

# Intentamos usar SQLAlchemy URL parser si está disponible
try:
    from sqlalchemy.engine import make_url
    have_make_url = True
except Exception:
    have_make_url = False

SCRIPT_TO_RUN = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'migrate_add_empleado_fields.py')


def parse_args():
    p = argparse.ArgumentParser(description='Wrapper: ejecutar migración de empleados usando app context')
    p.add_argument('--no-backup', action='store_true', help='No crear backup antes de migrar')
    p.add_argument('--no-yes', action='store_true', help='Pedir confirmación interactiva en el script de migración')
    p.add_argument('--config', default='development', help='Config de Flask (por defecto: development)')
    return p.parse_args()


def extract_pg_params(uri):
    # Devuelve dict con host, port, dbname, user, password (si disponibles)
    if not uri:
        return {}
    if have_make_url:
        try:
            url = make_url(uri)
            return {
                'host': url.host or 'localhost',
                'port': url.port or 5432,
                'dbname': url.database,
                'user': url.username,
                'password': url.password
            }
        except Exception:
            pass
    # Fallback: urlparse
    p = urlparse(uri)
    if p.scheme and 'postgres' in p.scheme:
        user = p.username
        password = p.password
        host = p.hostname or 'localhost'
        port = p.port or 5432
        dbname = p.path[1:] if p.path and p.path.startswith('/') else p.path
        return {'host': host, 'port': port, 'dbname': dbname, 'user': user, 'password': password}
    return {}


def main():
    args = parse_args()

    # Crear app y extraer URI
    app = create_app(args.config)
    with app.app_context():
        print('Aplicación cargada en modo:', args.config)
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print('SQLALCHEMY_DATABASE_URI encontrada:', bool(db_uri))

        params = extract_pg_params(db_uri)
        # Si la URI indica SQLite, ejecutamos el SQL directamente usando SQLAlchemy
        if db_uri and db_uri.startswith('sqlite'):
            print('Detectada base SQLite en SQLALCHEMY_DATABASE_URI — ejecutando SQL directamente vía SQLAlchemy')
            # Leer SQL (intentar utf-8, fallback latin-1)
            sql_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'add_empleado_fields.sql')
            if not os.path.exists(sql_file):
                print('No se encontró el archivo SQL en:', sql_file)
                sys.exit(2)
            sql_text = None
            try:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_text = f.read()
            except UnicodeDecodeError:
                with open(sql_file, 'r', encoding='latin-1') as f:
                    sql_text = f.read()

            engine = sqlalchemy.create_engine(db_uri)
            try:
                # Para SQLite es más fiable usar el raw connection y executescript
                raw = engine.raw_connection()
                try:
                    cur = raw.cursor()
                    cur.executescript(sql_text)
                    raw.commit()
                    print('SQL ejecutado correctamente sobre SQLite.')
                finally:
                    raw.close()
            except Exception as e:
                print('Error ejecutando SQL sobre SQLite:', e)
                sys.exit(1)

            return

        if not params or not params.get('dbname'):
            print('No se pudo extraer una conexión Postgres válida desde la config. Puedes ejecutar el script manualmente.')
            sys.exit(2)

        print('Parámetros extraídos:')
        print(f"  host: {params.get('host')}\n  port: {params.get('port')}\n  dbname: {params.get('dbname')}\n  user: {params.get('user')}")

        # Preparar entorno para el subprocess
        env = os.environ.copy()
        env['PGHOST'] = str(params.get('host'))
        env['PGPORT'] = str(params.get('port'))
        env['PGDATABASE'] = str(params.get('dbname'))
        if params.get('user'):
            env['PGUSER'] = str(params.get('user'))
        if params.get('password'):
            # PGPASSWORD es leído por nuestra herramienta; es una forma práctica para evitar prompt
            env['PGPASSWORD'] = str(params.get('password'))

        cmd = [sys.executable, SCRIPT_TO_RUN]
        if not args.no_backup:
            cmd.append('--backup')
        if args.no_yes:
            # si no-yes está presente, no añadimos --yes; por defecto el script pedirá confirmación
            pass
        else:
            cmd.append('--yes')

        print('\nEjecutando migración con comando:')
        print(' '.join(cmd))
        try:
            res = subprocess.run(cmd, env=env, check=True)
            print('\nMigración finalizada con código de salida:', res.returncode)
        except subprocess.CalledProcessError as e:
            print('\nError: el script de migración devolvió código', e.returncode)
            sys.exit(e.returncode)
        except Exception as e:
            print('\nExcepción al ejecutar el script de migración:', e)
            raise

if __name__ == '__main__':
    main()
