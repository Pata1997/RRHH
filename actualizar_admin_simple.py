# Script simple para actualizar el rol del usuario admin a ADMIN
import psycopg2

# Configuracion de la base de datos
DB_CONFIG = {
    'dbname': 'rrhh_db',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

try:
    # Conectar a PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("Conectado a PostgreSQL...")
    
    # Actualizar el usuario admin
    cur.execute("""
        UPDATE usuarios 
        SET rol = 'ADMIN' 
        WHERE nombre_usuario = 'admin'
    """)
    
    conn.commit()
    print("OK - Usuario admin actualizado con rol ADMIN")
    
    # Verificar
    cur.execute("""
        SELECT nombre_usuario, rol, activo 
        FROM usuarios 
        WHERE nombre_usuario = 'admin'
    """)
    
    result = cur.fetchone()
    if result:
        print(f"\nVerificacion:")
        print(f"  Usuario: {result[0]}")
        print(f"  Rol: {result[1]}")
        print(f"  Activo: {result[2]}")
    
    cur.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"Error de PostgreSQL: {e}")
except Exception as e:
    print(f"Error: {e}")
