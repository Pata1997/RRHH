#!/usr/bin/env python
"""Script para inicializar la BD y ejecutar migraciones."""
from app import create_app, db
import os

os.chdir(os.path.dirname(__file__))

app = create_app('development')

with app.app_context():
    print("Creando tablas de la BD...")
    db.create_all()
    print("✓ Tablas creadas exitosamente")
    
    # Ejecutar migración de despidos
    print("\nEjecutando migración de despidos...")
    os.system('python migrations/add_despido_table.py')
    
    print("\n✓ Inicialización completa")
