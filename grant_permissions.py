#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para otorgar permisos adicionales al usuario rrhh_user
"""

import psycopg2
from psycopg2 import sql

def grant_permissions():
    """Otorga permisos al usuario rrhh_user"""
    
    print("=" * 60)
    print("🔐 OTORGAR PERMISOS A rrhh_user")
    print("=" * 60)
    
    # Conectar como postgres (admin)
    conn = psycopg2.connect(
        user='postgres',
        password='123456',
        host='localhost',
        port=5432,
        dbname='rrhh_db'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        print("\n🔓 Otorgando permisos en esquema public...")
        
        # Otorgar permisos en el esquema
        cursor.execute("""
            GRANT ALL PRIVILEGES ON SCHEMA public TO rrhh_user;
        """)
        print("✓ Permisos en schema public otorgados")
        
        # Otorgar permisos por defecto para objetos futuros
        cursor.execute("""
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO rrhh_user;
        """)
        print("✓ Permisos por defecto en tablas otorgados")
        
        cursor.execute("""
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO rrhh_user;
        """)
        print("✓ Permisos por defecto en secuencias otorgados")
        
        cursor.execute("""
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO rrhh_user;
        """)
        print("✓ Permisos por defecto en funciones otorgados")
        
        cursor.execute("""
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO rrhh_user;
        """)
        print("✓ Permisos por defecto en tipos otorgados")
        
        # Otorgar permisos de conexión a la BD
        cursor.execute("""
            GRANT CONNECT ON DATABASE rrhh_db TO rrhh_user;
        """)
        print("✓ Permisos de conexión a BD otorgados")
        
        cursor.close()
        conn.close()
        
        print("\n✅ PERMISOS OTORGADOS EXITOSAMENTE")
        print("\n🚀 Próximo paso:")
        print("   python migrate_to_postgres.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        cursor.close()
        conn.close()
        return False

if __name__ == '__main__':
    grant_permissions()
