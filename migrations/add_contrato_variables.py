"""Agregar columna variables (JSON text) a la tabla contratos
Ejecución:
  python migrations\add_contrato_variables.py
"""
import os
import psycopg2
from urllib.parse import urlparse


def parse_database_url(database_url):
    parsed = urlparse(database_url)
    return {
        'user': parsed.username,
        'password': parsed.password or '',
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'database': parsed.path.lstrip('/') or 'rrhh_db'
    }


def main():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    database_url = os.environ.get('DATABASE_URL', '')
    if not database_url or not database_url.startswith('postgresql://'):
        print('DATABASE_URL no configurada en .env')
        return

    db_config = parse_database_url(database_url)
    print(f"Conectando a {db_config['user']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    try:
        conn = psycopg2.connect(host=db_config['host'], port=db_config['port'], user=db_config['user'], password=db_config['password'], database=db_config['database'])
        cursor = conn.cursor()

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='contratos' AND column_name='variables'
            )
        """)
        exists = cursor.fetchone()[0]
        if not exists:
            print('Añadiendo columna contratos.variables (TEXT)...')
            cursor.execute("ALTER TABLE contratos ADD COLUMN variables TEXT")
            conn.commit()
            print('Columna añadida')
        else:
            print('Columna contratos.variables ya existe')

        cursor.close()
        conn.close()
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    main()
