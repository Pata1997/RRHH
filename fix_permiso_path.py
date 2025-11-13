#!/usr/bin/env python
"""Script para limpiar la ruta del justificativo en la BD"""
from app import db, create_app
from app.models import Permiso

app = create_app()
with app.app_context():
    # Buscar permisos que tengan justificativo_archivo con ruta incorrecta
    permisos = Permiso.query.filter(Permiso.justificativo_archivo != None).all()
    
    for p in permisos:
        print(f"Permiso {p.id}: {p.justificativo_archivo}")
        # Si tiene 'uploads/uploads', arreglarlo
        if 'uploads/uploads' in p.justificativo_archivo:
            nueva_ruta = p.justificativo_archivo.replace('uploads/uploads', 'uploads')
            p.justificativo_archivo = nueva_ruta
            print(f"  -> Corregido a: {nueva_ruta}")
    
    db.session.commit()
    print("BD actualizada")
