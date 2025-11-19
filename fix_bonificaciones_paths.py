"""
Script para corregir las rutas de archivos de bonificaciones familiares
"""
import psycopg2

def fix_paths():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='rrhh_db',
        user='rrhh_user',
        password='123456'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Actualizando rutas de certificados...")
    
    # Actualizar rutas que empiezan con 'bonificaciones/' a 'uploads/bonificaciones/'
    cursor.execute("""
        UPDATE bonificaciones_familiares
        SET certificado_nacimiento = 'uploads/' || certificado_nacimiento
        WHERE certificado_nacimiento LIKE 'bonificaciones/%'
    """)
    
    cursor.execute("""
        UPDATE bonificaciones_familiares
        SET certificado_estudio = 'uploads/' || certificado_estudio
        WHERE certificado_estudio LIKE 'bonificaciones/%'
    """)
    
    cursor.execute("""
        UPDATE bonificaciones_familiares
        SET certificado_discapacidad = 'uploads/' || certificado_discapacidad
        WHERE certificado_discapacidad LIKE 'bonificaciones/%'
    """)
    
    print("✅ Rutas actualizadas correctamente")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    fix_paths()
