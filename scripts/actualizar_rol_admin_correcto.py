"""
Script para actualizar el rol del usuario admin a ADMIN
"""
from app import create_app
from app.models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Actualizando rol del usuario admin...")
    
    # Actualizar directamente con SQL
    db.session.execute(text("""
        UPDATE usuarios 
        SET rol = 'ADMIN' 
        WHERE nombre_usuario = 'admin'
    """))
    
    db.session.commit()
    print("✅ Usuario admin actualizado con rol 'ADMIN'")
    
    # Verificar
    result = db.session.execute(text("""
        SELECT nombre_usuario, rol, activo 
        FROM usuarios 
        WHERE nombre_usuario = 'admin'
    """)).fetchone()
    
    if result:
        print(f"\nVerificación:")
        print(f"  Usuario: {result[0]}")
        print(f"  Rol: {result[1]}")
        print(f"  Activo: {result[2]}")
