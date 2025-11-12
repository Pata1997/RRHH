"""Script para agregar columnas fecha_nacimiento y nivel_academico a postulantes"""
import os
import psycopg2
from urllib.parse import urlparse

def parse_database_url(database_url):
    """Parsea DATABASE_URL postgresql://user:pass@host:port/dbname"""
    parsed = urlparse(database_url)
    return {
        'user': parsed.username,
        'password': parsed.password or '',
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'database': parsed.path.lstrip('/') or 'rrhh_db'
    }

def main():
    # Cargar .env si existe
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    # Obtener DATABASE_URL
    database_url = os.environ.get('DATABASE_URL', '')
    
    if not database_url or not database_url.startswith('postgresql://'):
        print('❌ DATABASE_URL no está configurada o es inválida en .env')
        return
    
    # Parsear DATABASE_URL
    db_config = parse_database_url(database_url)
    
    print(f'🔌 Conectando a PostgreSQL: {db_config["user"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}')

    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()

        # Agregar columna fecha_nacimiento
        print('\n📋 Verificando columna postulantes.fecha_nacimiento...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='postulantes' AND column_name='fecha_nacimiento'
            )
        """)
        col_exists = cursor.fetchone()[0]

        if not col_exists:
            print('  → Agregando columna fecha_nacimiento...')
            cursor.execute('ALTER TABLE postulantes ADD COLUMN fecha_nacimiento DATE')
            conn.commit()
            print('  ✓ Columna fecha_nacimiento agregada')
        else:
            print('  ✓ Columna fecha_nacimiento ya existe')

        # Agregar columna nivel_academico
        print('\n📋 Verificando columna postulantes.nivel_academico...')
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='postulantes' AND column_name='nivel_academico'
            )
        """)
        col_exists = cursor.fetchone()[0]

        if not col_exists:
            print('  → Agregando columna nivel_academico...')
            cursor.execute('ALTER TABLE postulantes ADD COLUMN nivel_academico VARCHAR(120)')
            conn.commit()
            print('  ✓ Columna nivel_academico agregada')
        else:
            print('  ✓ Columna nivel_academico ya existe')

        print('\n' + '='*60)
        print('✅ ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!')
        print('='*60)
        print('\n🔄 Reinicia la aplicación Flask para que cargue los cambios.')
        print('   Ejecuta: python run.py')
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f'❌ Error: {str(e)}')
        return

if __name__ == '__main__':
    main()
