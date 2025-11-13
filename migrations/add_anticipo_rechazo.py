#!/usr/bin/env python
"""Migración para agregar campos de rechazo al modelo Anticipo"""

import os
import sys
from sqlalchemy import text, inspect
from dotenv import load_dotenv

# Cargar variables de entorno desde .env para asegurar que la migración
# se ejecute contra la misma base de datos que la aplicación.
load_dotenv()

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

app = create_app()

with app.app_context():
    try:
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('anticipos')]
        
        print("Columnas actuales en tabla anticipos:")
        for col in columns:
            print(f"  - {col}")
        
        # Agregar columnas si no existen
        if 'rechazado' not in columns:
            print("\n✓ Agregando columna 'rechazado'...")
            db.session.execute(text('ALTER TABLE anticipos ADD COLUMN rechazado BOOLEAN DEFAULT FALSE'))
            print("✓ Columna 'rechazado' agregada")
        
        if 'rechazado_por' not in columns:
            print("✓ Agregando columna 'rechazado_por'...")
            db.session.execute(text('ALTER TABLE anticipos ADD COLUMN rechazado_por INTEGER REFERENCES usuarios(id)'))
            print("✓ Columna 'rechazado_por' agregada")
        
        if 'fecha_rechazo' not in columns:
            print("✓ Agregando columna 'fecha_rechazo'...")
            db.session.execute(text('ALTER TABLE anticipos ADD COLUMN fecha_rechazo TIMESTAMP'))
            print("✓ Columna 'fecha_rechazo' agregada")
        
        db.session.commit()
        print("\n✓ Migración completada exitosamente")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error durante la migración: {str(e)}")
        sys.exit(1)
