#!/usr/bin/env python3
"""
Script de migración para agregar campos IPS a Empresa y Cargo.
Ejecuta: python scripts/migrate_ips_campos.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def run_migration():
    app = create_app()
    with app.app_context():
        try:
            # Agregar numero_patronal a empresas
            db.session.execute(db.text("""
                ALTER TABLE empresas 
                ADD COLUMN numero_patronal VARCHAR(50) NULL;
            """))
            print("✓ Columna numero_patronal agregada a tabla empresas")
        except Exception as e:
            if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                print("⊘ Columna numero_patronal ya existe en empresas")
            else:
                print(f"✗ Error al agregar numero_patronal: {e}")
        
        try:
            # Agregar categoria_ips a cargos
            db.session.execute(db.text("""
                ALTER TABLE cargos 
                ADD COLUMN categoria_ips VARCHAR(10) DEFAULT '01' NULL;
            """))
            print("✓ Columna categoria_ips agregada a tabla cargos")
        except Exception as e:
            if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                print("⊘ Columna categoria_ips ya existe en cargos")
            else:
                print(f"✗ Error al agregar categoria_ips: {e}")
        
        db.session.commit()
        print("\n✅ Migración completada exitosamente")

if __name__ == '__main__':
    run_migration()
