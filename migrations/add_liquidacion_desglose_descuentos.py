"""
Migración: Agregar campos de desglose de descuentos a liquidaciones
Fecha: 2025-01
Objetivo: Permitir ver el detalle de descuentos en los recibos de salario
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from app import create_app, db

def add_descuentos_desglose():
    # Forzar el entorno a production para usar PostgreSQL
    app = create_app('production')
    with app.app_context():
        try:
            print(f"🔍 Conectado a: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Unknown')[:50]}...")
            
            # Agregar columnas para desglose de descuentos (PostgreSQL)
            alterations = [
                "ALTER TABLE liquidaciones ADD COLUMN IF NOT EXISTS descuento_ausencias NUMERIC(12, 2) DEFAULT 0",
                "ALTER TABLE liquidaciones ADD COLUMN IF NOT EXISTS descuento_anticipos NUMERIC(12, 2) DEFAULT 0",
                "ALTER TABLE liquidaciones ADD COLUMN IF NOT EXISTS descuento_sanciones NUMERIC(12, 2) DEFAULT 0",
                "ALTER TABLE liquidaciones ADD COLUMN IF NOT EXISTS descuento_otros NUMERIC(12, 2) DEFAULT 0",
            ]
            
            for sql in alterations:
                print(f"  Ejecutando: {sql[:60]}...")
                db.session.execute(text(sql))
            
            db.session.commit()
            print("\n✅ Migración completada: Campos de desglose agregados a liquidaciones")
            print("   - descuento_ausencias: Para ausencias injustificadas")
            print("   - descuento_anticipos: Para anticipos de sueldo")
            print("   - descuento_sanciones: Para sanciones monetarias")
            print("   - descuento_otros: Para descuentos manuales adicionales")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error en migración: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    add_descuentos_desglose()
