#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para limpiar y recrear la base de datos PostgreSQL
"""

import psycopg2
from psycopg2 import sql

def clean_and_recreate_db():
    """Elimina todas las tablas y recrear vacías"""
    
    print("=" * 60)
    print("🗑️  LIMPIAR BASE DE DATOS PostgreSQL")
    print("=" * 60)
    
    # Conexión
    conn = psycopg2.connect(
        user='rrhh_user',
        password='123456',
        host='localhost',
        port=5432,
        dbname='rrhh_db'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        print("\n📋 Obteniendo lista de tablas...")
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = cursor.fetchall()
        
        if not tables:
            print("ℹ️  No hay tablas para eliminar")
        else:
            print(f"✓ Encontradas {len(tables)} tablas")
            
            # Eliminar todas las tablas
            print("\n🗑️  Eliminando tablas...")
            cursor.execute("DROP SCHEMA public CASCADE")
            cursor.execute("CREATE SCHEMA public")
            print("✓ Esquema eliminado y recreado")
        
        cursor.close()
        conn.close()
        
        print("\n✅ BASE DE DATOS LIMPIA")
        print("\n🚀 Próximo paso:")
        print("   python init_database.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        cursor.close()
        conn.close()
        return False

if __name__ == '__main__':
    clean_and_recreate_db()
