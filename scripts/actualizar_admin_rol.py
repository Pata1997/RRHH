"""
Script para actualizar el rol del usuario admin de RRHH a ADMIN
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Forzar configuración de producción para PostgreSQL
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from app.models import Usuario, RoleEnum

app = create_app('production')

with app.app_context():
    print('='*70)
    print('🔧 ACTUALIZANDO ROL DEL USUARIO ADMIN')
    print('='*70)
    
    # Buscar usuario admin
    admin = Usuario.query.filter_by(nombre_usuario='admin').first()
    
    if admin:
        print(f'\n✓ Usuario encontrado: {admin.nombre_usuario}')
        print(f'  Nombre completo: {admin.nombre_completo}')
        print(f'  Email: {admin.email}')
        print(f'  Rol actual: {admin.rol.name}')
        
        if admin.rol == RoleEnum.ADMIN:
            print('\n✅ El usuario ya tiene rol ADMIN. No se necesita actualización.')
        else:
            print(f'\n🔄 Cambiando rol de {admin.rol.name} a ADMIN...')
            admin.rol = RoleEnum.ADMIN
            db.session.commit()
            print('✅ Rol actualizado correctamente a ADMIN')
    else:
        print('\n❌ Usuario "admin" no encontrado en la base de datos')
        print('   Ejecuta run.py para crear el usuario admin')
    
    print('\n' + '='*70)
    print('✅ PROCESO COMPLETADO')
    print('='*70)
    print('\nAhora puedes:')
    print('1. Cerrar sesión en el navegador')
    print('2. Iniciar sesión nuevamente con: admin / admin123')
    print('3. Verás el menú "Usuarios" en la barra de navegación')
