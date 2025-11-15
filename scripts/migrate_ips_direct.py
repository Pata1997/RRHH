#!/usr/bin/env python3
"""
Script directo de migración para agregar campos IPS.
Ejecuta SQL directamente contra PostgreSQL.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def run_migration():
    app = create_app()
    with app.app_context():
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        
        try:
            # Agregar numero_patronal a empresas
            sql1 = "ALTER TABLE empresas ADD COLUMN numero_patronal VARCHAR(50);"
            cursor.execute(sql1)
            print("✓ Columna numero_patronal agregada a tabla empresas")
        except Exception as e:
            print(f"Nota: {e}")
        
        try:
            # Agregar categoria_ips a cargos
            sql2 = "ALTER TABLE cargos ADD COLUMN categoria_ips VARCHAR(10) DEFAULT '01';"
            cursor.execute(sql2)
            print("✓ Columna categoria_ips agregada a tabla cargos")
        except Exception as e:
            print(f"Nota: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("\n✅ Migración SQL ejecutada")

if __name__ == '__main__':
    run_migration()
