"""
Migración: Agregar campos de justificación a tabla asistencias
Fecha: 2025-11-19
Descripción: Permite a RRHH justificar o no justificar ausencias detectadas automáticamente
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from sqlalchemy import text

def upgrade():
    """Agregar campos de justificación"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n🔧 Agregando campos de justificación a tabla asistencias (PostgreSQL)...")
            
            # 1. Crear ENUM para estado de justificación
            print("1️⃣ Creando ENUM justificacion_estado_enum...")
            try:
                db.session.execute(text("""
                    DO $$ BEGIN
                        CREATE TYPE justificacion_estado_enum AS ENUM ('PENDIENTE', 'JUSTIFICADO', 'INJUSTIFICADO');
                    EXCEPTION
                        WHEN duplicate_object THEN null;
                    END $$;
                """))
                db.session.commit()
                print("   ✅ ENUM creado")
            except Exception as e:
                print(f"   ⚠️ ENUM ya existe")
                db.session.rollback()
            
            # 2. Agregar columna justificacion_estado
            print("2️⃣ Agregando columna justificacion_estado...")
            try:
                db.session.execute(text("""
                    ALTER TABLE asistencias 
                    ADD COLUMN IF NOT EXISTS justificacion_estado justificacion_estado_enum DEFAULT 'PENDIENTE';
                """))
                db.session.commit()
                print("   ✅ Columna justificacion_estado agregada")
            except Exception as e:
                print(f"   ⚠️ Columna ya existe")
                db.session.rollback()
            
            # 3. Agregar columna justificacion_nota
            print("3️⃣ Agregando columna justificacion_nota...")
            try:
                db.session.execute(text("""
                    ALTER TABLE asistencias 
                    ADD COLUMN IF NOT EXISTS justificacion_nota TEXT;
                """))
                db.session.commit()
                print("   ✅ Columna justificacion_nota agregada")
            except Exception as e:
                print(f"   ⚠️ Columna ya existe")
                db.session.rollback()
            
            # 4. Agregar columna justificacion_fecha
            print("4️⃣ Agregando columna justificacion_fecha...")
            try:
                db.session.execute(text("""
                    ALTER TABLE asistencias 
                    ADD COLUMN IF NOT EXISTS justificacion_fecha TIMESTAMP;
                """))
                db.session.commit()
                print("   ✅ Columna justificacion_fecha agregada")
            except Exception as e:
                print(f"   ⚠️ Columna ya existe")
                db.session.rollback()
            
            # 5. Agregar columna justificacion_por (FK a usuarios)
            print("5️⃣ Agregando columna justificacion_por...")
            try:
                db.session.execute(text("""
                    ALTER TABLE asistencias 
                    ADD COLUMN IF NOT EXISTS justificacion_por INTEGER REFERENCES usuarios(id);
                """))
                db.session.commit()
                print("   ✅ Columna justificacion_por agregada")
            except Exception as e:
                print(f"   ⚠️ Columna ya existe")
                db.session.rollback()
            
            # 6. Actualizar registros existentes con presente=TRUE a NULL (no necesitan justificación)
            print("6️⃣ Actualizando registros existentes...")
            db.session.execute(text("""
                UPDATE asistencias 
                SET justificacion_estado = NULL 
                WHERE presente = TRUE;
            """))
            db.session.commit()
            print("   ✅ Registros actualizados")
            
            print("\n✅ Migración completada exitosamente!")
            print("\nColumnas agregadas:")
            print("  - justificacion_estado (ENUM: PENDIENTE, JUSTIFICADO, INJUSTIFICADO)")
            print("  - justificacion_nota (TEXT)")
            print("  - justificacion_fecha (TIMESTAMP)")
            print("  - justificacion_por (INTEGER FK → usuarios.id)")
            
        except Exception as e:
            print(f"\n❌ Error en migración: {e}")
            db.session.rollback()
            raise

def downgrade():
    """Revertir cambios (PostgreSQL)"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n🔧 Revirtiendo migración...")
            
            db.session.execute(text("ALTER TABLE asistencias DROP COLUMN IF EXISTS justificacion_por;"))
            db.session.execute(text("ALTER TABLE asistencias DROP COLUMN IF EXISTS justificacion_fecha;"))
            db.session.execute(text("ALTER TABLE asistencias DROP COLUMN IF EXISTS justificacion_nota;"))
            db.session.execute(text("ALTER TABLE asistencias DROP COLUMN IF EXISTS justificacion_estado;"))
            db.session.execute(text("DROP TYPE IF EXISTS justificacion_estado_enum;"))
            
            db.session.commit()
            print("✅ Migración revertida")
            
        except Exception as e:
            print(f"❌ Error al revertir: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    upgrade()
