#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para crear la base de datos PostgreSQL y usuario automáticamente.

Requisitos:
  - PostgreSQL debe estar instalado y corriendo
  - python-dotenv y psycopg2 deben estar instalados (pip install -r requirements.txt)

Uso:
    python setup_postgres.py
"""

import psycopg2
from psycopg2 import sql
import os
import sys

def setup_postgres():
    """Crea la base de datos y usuario en PostgreSQL"""
    
    print("=" * 60)
    print("🐘 SETUP PostgreSQL para RRHH 2.0")
    print("=" * 60)
    
    # Parámetros de conexión (usar conexión por defecto de PostgreSQL)
    default_user = "postgres"
    default_password = input("\n¿Contraseña del usuario 'postgres'? (presiona Enter si no hay): ").strip() or None
    default_host = "localhost"
    default_port = 5432
    
    # Parámetros para crear
    new_db = "rrhh_db"
    new_user = "rrhh_user"
    new_password = "123456"
    
    # Intentar conectar como postgres
    try:
        print(f"\n📡 Conectando a PostgreSQL como '{default_user}'...")
        
        conn_params = {
            'user': default_user,
            'password': default_password,
            'host': default_host,
            'port': default_port,
            'dbname': 'postgres'
        }
        
        # Remover password si es None
        if conn_params['password'] is None:
            del conn_params['password']
        
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True  # Necesario para CREATE DATABASE
        cursor = conn.cursor()
        
        print(f"✓ Conectado a PostgreSQL como '{default_user}'")
        
        # ==================== CREAR BASE DE DATOS ====================
        print(f"\n📦 Creando base de datos '{new_db}'...")
        
        try:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(new_db)
            ))
            print(f"✓ Base de datos '{new_db}' creada")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ℹ️  Base de datos '{new_db}' ya existe")
        
        # ==================== CREAR USUARIO ====================
        print(f"\n👤 Creando usuario '{new_user}'...")
        
        try:
            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                sql.Identifier(new_user)
            ), (new_password,))
            print(f"✓ Usuario '{new_user}' creado")
        except psycopg2.errors.DuplicateObject:
            print(f"ℹ️  Usuario '{new_user}' ya existe")
            # Cambiar contraseña
            print(f"🔄 Actualizando contraseña...")
            cursor.execute(sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
                sql.Identifier(new_user)
            ), (new_password,))
            print(f"✓ Contraseña actualizada")
        
        # ==================== CONFIGURAR USUARIO ====================
        print(f"\n⚙️  Configurando rol '{new_user}'...")
        
        cursor.execute(sql.SQL("ALTER ROLE {} SET client_encoding TO 'utf8'").format(
            sql.Identifier(new_user)
        ))
        
        cursor.execute(sql.SQL("ALTER ROLE {} SET default_transaction_isolation TO 'read committed'").format(
            sql.Identifier(new_user)
        ))
        
        cursor.execute(sql.SQL("ALTER ROLE {} SET default_transaction_deferrable TO on").format(
            sql.Identifier(new_user)
        ))
        
        print(f"✓ Configuración aplicada")
        
        # ==================== OTORGAR PERMISOS ====================
        print(f"\n🔐 Otorgando permisos al usuario...")
        
        cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(new_db),
            sql.Identifier(new_user)
        ))
        
        print(f"✓ Permisos otorgados")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        # ==================== VERIFICACIÓN ====================
        print(f"\n✅ Verificando conexión con '{new_user}'...")
        
        try:
            conn_test = psycopg2.connect(
                user=new_user,
                password=new_password,
                host=default_host,
                port=default_port,
                dbname=new_db
            )
            conn_test.close()
            print(f"✓ Conexión exitosa como '{new_user}' a '{new_db}'")
        except Exception as e:
            print(f"⚠️  Error al verificar conexión: {e}")
            return False
        
        # ==================== RESUMEN ====================
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"\n📊 Credenciales configuradas:")
        print(f"   Host: {default_host}")
        print(f"   Puerto: {default_port}")
        print(f"   Base de datos: {new_db}")
        print(f"   Usuario: {new_user}")
        print(f"   Contraseña: {new_password}")
        
        print(f"\n📝 DATABASE_URL para .env:")
        print(f"   postgresql://{new_user}:{new_password}@{default_host}:{default_port}/{new_db}")
        
        print(f"\n🚀 Próximos pasos:")
        print(f"   1. python init_database.py  (crear tablas)")
        print(f"   2. python run.py             (iniciar servidor)")
        print(f"   3. Acceder a http://localhost:5000")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Error de conexión a PostgreSQL: {e}")
        print(f"\n💡 Asegúrate de que:")
        print(f"   1. PostgreSQL esté instalado")
        print(f"   2. El servicio PostgreSQL esté corriendo")
        print(f"   3. La contraseña de 'postgres' sea correcta")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = setup_postgres()
    sys.exit(0 if success else 1)
