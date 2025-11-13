#!/usr/bin/env python
"""Migración para crear tabla de empresas"""

import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

app = create_app()

with app.app_context():
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        # Verificar si la tabla ya existe
        if 'empresas' not in inspector.get_table_names():
            print("✓ Creando tabla 'empresas'...")
            
            # Crear la tabla using SQLAlchemy ORM
            db.create_all()
            
            print("✓ Tabla 'empresas' creada exitosamente")
        else:
            print("✓ Tabla 'empresas' ya existe")
            
            # Verificar si faltan columnas
            columns = [col['name'] for col in inspector.get_columns('empresas')]
            expected_columns = [
                'id', 'nombre', 'ruc', 'direccion', 'telefono', 'email', 
                'logo_path', 'razon_social', 'pais', 'ciudad', 'representante_legal', 
                'ci_representante', 'porcentaje_ips_empleado', 'porcentaje_ips_empleador', 
                'dias_habiles_mes', 'fecha_creacion', 'fecha_actualizacion'
            ]
            
            for col in expected_columns:
                if col not in columns:
                    print(f"  ⚠ Falta columna: {col}")
            
            if set(expected_columns).issubset(set(columns)):
                print("✓ Todas las columnas esperadas están presentes")
        
        db.session.commit()
        print("\n✓ Migración completada exitosamente")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error durante la migración: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
