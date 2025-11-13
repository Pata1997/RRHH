#!/usr/bin/env python
"""Script para verificar las rutas de justificativos en la BD"""
import os
from app import db, create_app
from app.models import Permiso

app = create_app()
with app.app_context():
    # Buscar permisos que tengan justificativo_archivo
    permisos = Permiso.query.filter(Permiso.justificativo_archivo != None).all()
    
    print("=== Permisos con justificativo ===")
    for p in permisos:
        ruta_bd = p.justificativo_archivo
        ruta_completa = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', ruta_bd)
        existe = os.path.exists(ruta_completa)
        print(f"\nPermiso {p.id}:")
        print(f"  Ruta en BD: {ruta_bd}")
        print(f"  Ruta completa: {ruta_completa}")
        print(f"  ¿Existe?: {existe}")
        
        # Si la ruta contiene 'uploads/uploads', corregirla
        if 'uploads/uploads' in ruta_bd:
            nueva_ruta = ruta_bd.replace('uploads/uploads', 'uploads')
            print(f"  CORRIGIENDO a: {nueva_ruta}")
            p.justificativo_archivo = nueva_ruta
    
    if any('uploads/uploads' in (p.justificativo_archivo or '') for p in permisos):
        db.session.commit()
        print("\n✓ BD actualizada")
    else:
        print("\n✓ No hay rutas duplicadas para corregir")
