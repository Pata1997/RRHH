"""
Migración: Agregar valor ADMIN al enum roleenum en PostgreSQL
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Forzar configuración de producción para PostgreSQL
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from sqlalchemy import text

app = create_app('production')

with app.app_context():
    print('='*70)
    print('🔧 AGREGANDO VALOR "ADMIN" AL ENUM roleenum')
    print('='*70)
    
    try:
        # Verificar si ADMIN ya existe en el enum
        result = db.session.execute(text("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'roleenum')
        """))
        
        valores_actuales = [row[0] for row in result]
        print(f'\n📋 Valores actuales en roleenum: {valores_actuales}')
        
        if 'Administrador' in valores_actuales or 'ADMIN' in valores_actuales:
            print('\n✅ El valor ADMIN ya existe en el enum')
        else:
            print('\n🔄 Agregando valor "Administrador" al enum...')
            
            # Agregar el nuevo valor al enum
            db.session.execute(text("""
                ALTER TYPE roleenum ADD VALUE 'Administrador' BEFORE 'RRHH'
            """))
            db.session.commit()
            
            print('✅ Valor "Administrador" agregado exitosamente al enum')
        
        # Ahora actualizar el usuario admin
        print('\n🔄 Actualizando rol del usuario admin...')
        db.session.execute(text("""
            UPDATE usuarios SET rol = 'Administrador' WHERE nombre_usuario = 'admin'
        """))
        db.session.commit()
        
        print('✅ Usuario admin actualizado a rol Administrador')
        
    except Exception as e:
        db.session.rollback()
        print(f'\n❌ Error: {e}')
        print('\nIntentando método alternativo...')
        
        try:
            # Método alternativo: Agregar al final
            db.session.execute(text("""
                ALTER TYPE roleenum ADD VALUE IF NOT EXISTS 'Administrador'
            """))
            db.session.commit()
            
            db.session.execute(text("""
                UPDATE usuarios SET rol = 'Administrador' WHERE nombre_usuario = 'admin'
            """))
            db.session.commit()
            
            print('✅ Actualización exitosa con método alternativo')
            
        except Exception as e2:
            db.session.rollback()
            print(f'\n❌ Error en método alternativo: {e2}')
    
    print('\n' + '='*70)
    print('✅ PROCESO COMPLETADO')
    print('='*70)
    print('\n📝 Pasos siguientes:')
    print('1. Cierra sesión en el navegador')
    print('2. Inicia sesión con: admin / admin123')
    print('3. Verás el menú "🛡️ Usuarios"')
