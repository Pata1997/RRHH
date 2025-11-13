#!/usr/bin/env python
"""Script para ver exactamente qué está guardado en justificativo_archivo"""
from app import db, create_app
from app.models import Permiso

app = create_app()
with app.app_context():
    permisos = Permiso.query.filter(Permiso.justificativo_archivo != None).all()
    
    print("=== Contenido exacto de justificativo_archivo ===")
    for p in permisos:
        print(f"Permiso {p.id}: '{p.justificativo_archivo}'")
