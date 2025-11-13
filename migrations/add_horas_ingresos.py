#!/usr/bin/env python
"""Migración para crear tabla horas_extras y actualizar ingresos_extras"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

app = create_app()

with app.app_context():
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        # Crear tabla horas_extras si no existe
        if 'horas_extras' not in tables:
            print('✓ Creando tabla horas_extras...')
            # Usar ORM create_all para crear la nueva tabla basada en modelos
            db.create_all()
            print('✓ Tabla horas_extras creada')
        else:
            print('✓ Tabla horas_extras ya existe')

        # Verificar columnas en ingresos_extras y agregar las que faltan
        cols = [c['name'] for c in inspector.get_columns('ingresos_extras')]
        alterations = []
        if 'estado' not in cols:
            alterations.append("ALTER TABLE ingresos_extras ADD COLUMN estado VARCHAR(20) DEFAULT 'PENDIENTE'")
        if 'creado_por' not in cols:
            alterations.append('ALTER TABLE ingresos_extras ADD COLUMN creado_por INTEGER')
        if 'aplicado' not in cols:
            alterations.append('ALTER TABLE ingresos_extras ADD COLUMN aplicado BOOLEAN DEFAULT FALSE')
        if 'fecha_aplicacion' not in cols:
            alterations.append('ALTER TABLE ingresos_extras ADD COLUMN fecha_aplicacion TIMESTAMP')
        if 'justificativo_archivo' not in cols:
            alterations.append("ALTER TABLE ingresos_extras ADD COLUMN justificativo_archivo VARCHAR(255)")

        for stmt in alterations:
            print('✓ Ejecutando:', stmt)
            db.session.execute(text(stmt))

        db.session.commit()
        print('\n✓ Migración completada exitosamente')
    except Exception as e:
        db.session.rollback()
        print('❌ Error durante la migración:', str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)
