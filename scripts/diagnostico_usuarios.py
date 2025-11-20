"""
Script de diagnóstico para verificar roles de usuarios
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
    print('🔍 DIAGNÓSTICO DE USUARIOS Y ROLES')
    print('='*70)
    
    usuarios = Usuario.query.all()
    
    print(f'\n📊 Total de usuarios: {len(usuarios)}\n')
    
    for usuario in usuarios:
        print(f'Usuario: {usuario.nombre_usuario}')
        print(f'  Nombre: {usuario.nombre_completo}')
        print(f'  Email: {usuario.email}')
        print(f'  Rol: {usuario.rol.name}')
        print(f'  Activo: {"Sí" if usuario.activo else "No"}')
        if usuario.ultimo_login:
            print(f'  Último login: {usuario.ultimo_login.strftime("%d/%m/%Y %H:%M")}')
        else:
            print(f'  Último login: Nunca')
        print('-' * 70)
    
    print('\n' + '='*70)
    print('💡 SOLUCIÓN')
    print('='*70)
    
    admin = Usuario.query.filter_by(nombre_usuario='admin').first()
    
    if admin:
        if admin.rol != RoleEnum.ADMIN:
            print(f'\n⚠️  El usuario "admin" tiene rol: {admin.rol.name}')
            print(f'   Debe tener rol: ADMIN')
            print('\n🔧 Para corregirlo, ejecuta:')
            print('   python scripts\\actualizar_admin_rol.py')
        else:
            print(f'\n✅ El usuario "admin" tiene rol ADMIN correcto')
            print('\n🔍 Si no ves el menú "Usuarios", verifica:')
            print('   1. ¿Cerraste sesión y volviste a entrar?')
            print('   2. ¿Iniciaste sesión con el usuario "admin"?')
            print('   3. Limpia la caché del navegador (Ctrl+Shift+R)')
    else:
        print('\n❌ No existe usuario "admin"')
        print('   Ejecuta: python run.py')
        print('   Esto creará el usuario admin con rol ADMIN')
