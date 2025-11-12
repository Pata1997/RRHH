#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para inicializar la base de datos con datos de prueba

Uso:
    python init_database.py
"""

import os
import sys
from datetime import datetime, date, timedelta
from decimal import Decimal
from dotenv import load_dotenv

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    Usuario, Cargo, Empleado, Asistencia, Permiso, 
    Sancion, Liquidacion, Vacacion, RoleEnum, EstadoEmpleadoEnum,
    EstadoPermisoEnum, EstadoVacacionEnum
)

def init_database():
    """Inicializa la base de datos con datos de prueba"""
    
    # Si no existe .env, crear una copia desde .env.example para facilitar configuración
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_example_path = os.path.join(os.path.dirname(__file__), '.env.example')
    if not os.path.exists(env_path) and os.path.exists(env_example_path):
        print(".env no encontrado — creando desde .env.example (revísalo y ajusta credenciales)")
        try:
            with open(env_example_path, 'r', encoding='utf-8') as src, open(env_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print("Se creó .env desde .env.example")
        except Exception as e:
            print(f"Error al crear .env desde .env.example: {e}")

    # Cargar variables de entorno desde .env si existe
    load_dotenv()

    # Mostrar la URL de conexión para diagnóstico (repr para ver bytes especiales)
    print("DEBUG: DATABASE_URL repr:", repr(os.environ.get('DATABASE_URL')))

    # IMPORTANTE: Para init_database, forzar el uso de PostgreSQL (no SQLite)
    # Temporalmente establecer la variable para que DevelopmentConfig la use
    if not os.environ.get('DATABASE_URL'):
        print("⚠️  ERROR: DATABASE_URL no está definida en .env")
        print("   Debe contener: postgresql://rrhh_user:123456@localhost:5432/rrhh_db")
        sys.exit(1)

    app = create_app('development')
    
    with app.app_context():
        # Crear todas las tablas
        print("📦 Creando tablas de base de datos...")
        db.create_all()
        
        # Limpiar datos existentes (opcional)
        # print("🗑️  Limpiando datos existentes...")
        # db.session.query(Usuario).delete()
        # db.session.query(Cargo).delete()
        # db.session.query(Empleado).delete()
        # db.session.commit()
        
        # ==================== USUARIOS ====================
        print("👤 Creando usuarios...")
        
        usuarios_existentes = Usuario.query.count()
        if usuarios_existentes == 0:
            usuario_admin = Usuario(
                nombre_usuario='admin',
                email='admin@cooperativa.com',
                nombre_completo='Administrador del Sistema',
                rol=RoleEnum.RRHH,
                activo=True
            )
            usuario_admin.set_password('admin123')
            db.session.add(usuario_admin)
            
            usuario_asistente = Usuario(
                nombre_usuario='asistente',
                email='asistente@cooperativa.com',
                nombre_completo='Asistente de Recursos Humanos',
                rol=RoleEnum.ASISTENTE_RRHH,
                activo=True
            )
            usuario_asistente.set_password('asistente123')
            db.session.add(usuario_asistente)
            
            db.session.commit()
            print("  ✓ Usuarios creados")
        else:
            print("  ℹ️  Los usuarios ya existen")
        
        # ==================== CARGOS ====================
        print("💼 Creando cargos...")
        
        cargos_existentes = Cargo.query.count()
        if cargos_existentes == 0:
            cargos_data = [
                {
                    'nombre': 'Gerente General',
                    'descripcion': 'Gerente General responsable de toda la cooperativa',
                    'salario_base': Decimal('5000000')
                },
                {
                    'nombre': 'Contador',
                    'descripcion': 'Contador responsable de finanzas y contabilidad',
                    'salario_base': Decimal('3000000')
                },
                {
                    'nombre': 'Especialista RRHH',
                    'descripcion': 'Especialista en Recursos Humanos',
                    'salario_base': Decimal('2500000')
                },
                {
                    'nombre': 'Técnico de Operaciones',
                    'descripcion': 'Técnico responsable de operaciones diarias',
                    'salario_base': Decimal('2000000')
                },
                {
                    'nombre': 'Operario',
                    'descripcion': 'Operario de producción',
                    'salario_base': Decimal('1500000')
                },
                {
                    'nombre': 'Asistente Administrativo',
                    'descripcion': 'Asistente de tareas administrativas',
                    'salario_base': Decimal('1200000')
                },
            ]
            
            for cargo_data in cargos_data:
                cargo = Cargo(**cargo_data, fecha_creacion=datetime.utcnow())
                db.session.add(cargo)
            
            db.session.commit()
            print(f"  ✓ {len(cargos_data)} cargos creados")
        else:
            print("  ℹ️  Los cargos ya existen")
        
        # ==================== EMPLEADOS ====================
        print("👥 Creando empleados...")
        
        empleados_existentes = Empleado.query.count()
        if empleados_existentes == 0:
            # Obtener cargos
            gerente = Cargo.query.filter_by(nombre='Gerente General').first()
            contador = Cargo.query.filter_by(nombre='Contador').first()
            especialista = Cargo.query.filter_by(nombre='Especialista RRHH').first()
            tecnico = Cargo.query.filter_by(nombre='Técnico de Operaciones').first()
            operario = Cargo.query.filter_by(nombre='Operario').first()
            asistente = Cargo.query.filter_by(nombre='Asistente Administrativo').first()
            
            empleados_data = [
                {
                    'codigo': 'EMP001',
                    'nombre': 'Juan',
                    'apellido': 'García López',
                    'ci': '1234567',
                    'email': 'juan.garcia@cooperativa.com',
                    'telefono': '+595 991 234567',
                    'cargo_id': gerente.id,
                    'salario_base': gerente.salario_base,
                    'fecha_ingreso': date(2020, 1, 15),
                    'fecha_nacimiento': date(1985, 5, 10),
                    'sexo': 'M',
                    'direccion': 'Av. Principal 123, Asunción',
                    'estado': EstadoEmpleadoEnum.ACTIVO
                },
                {
                    'codigo': 'EMP002',
                    'nombre': 'María',
                    'apellido': 'López Martínez',
                    'ci': '1234568',
                    'email': 'maria.lopez@cooperativa.com',
                    'telefono': '+595 991 234568',
                    'cargo_id': contador.id,
                    'salario_base': contador.salario_base,
                    'fecha_ingreso': date(2021, 3, 20),
                    'fecha_nacimiento': date(1987, 8, 22),
                    'sexo': 'F',
                    'direccion': 'Calle Principal 456, Asunción',
                    'estado': EstadoEmpleadoEnum.ACTIVO
                },
                {
                    'codigo': 'EMP003',
                    'nombre': 'Carlos',
                    'apellido': 'Rodríguez Silva',
                    'ci': '1234569',
                    'email': 'carlos.rodriguez@cooperativa.com',
                    'telefono': '+595 991 234569',
                    'cargo_id': especialista.id,
                    'salario_base': especialista.salario_base,
                    'fecha_ingreso': date(2022, 6, 10),
                    'fecha_nacimiento': date(1990, 3, 15),
                    'sexo': 'M',
                    'direccion': 'Pasaje Secundario 789, Asunción',
                    'estado': EstadoEmpleadoEnum.ACTIVO
                },
                {
                    'codigo': 'EMP004',
                    'nombre': 'Ana',
                    'apellido': 'Fernández Gómez',
                    'ci': '1234570',
                    'email': 'ana.fernandez@cooperativa.com',
                    'telefono': '+595 991 234570',
                    'cargo_id': operario.id,
                    'salario_base': operario.salario_base,
                    'fecha_ingreso': date(2023, 1, 5),
                    'fecha_nacimiento': date(1992, 11, 28),
                    'sexo': 'F',
                    'direccion': 'Avenida Secundaria 321, Asunción',
                    'estado': EstadoEmpleadoEnum.ACTIVO
                },
                {
                    'codigo': 'EMP005',
                    'nombre': 'Pedro',
                    'apellido': 'González Torres',
                    'ci': '1234571',
                    'email': 'pedro.gonzalez@cooperativa.com',
                    'telefono': '+595 991 234571',
                    'cargo_id': asistente.id,
                    'salario_base': asistente.salario_base,
                    'fecha_ingreso': date(2023, 6, 15),
                    'fecha_nacimiento': date(1995, 2, 8),
                    'sexo': 'M',
                    'direccion': 'Calle Terciaria 654, Asunción',
                    'estado': EstadoEmpleadoEnum.ACTIVO
                },
            ]
            
            for emp_data in empleados_data:
                empleado = Empleado(**emp_data, fecha_creacion=datetime.utcnow())
                db.session.add(empleado)
            
            db.session.commit()
            print(f"  ✓ {len(empleados_data)} empleados creados")
        else:
            print("  ℹ️  Los empleados ya existen")
        
        # ==================== ASISTENCIAS ====================
        print("📅 Creando asistencias de ejemplo...")
        
        asistencias_existentes = Asistencia.query.count()
        if asistencias_existentes == 0:
            empleados = Empleado.query.all()
            fecha_base = date.today() - timedelta(days=10)
            
            contador_asistencias = 0
            for empleado in empleados:
                for i in range(10):
                    fecha = fecha_base + timedelta(days=i)
                    
                    # Evitar fines de semana
                    if fecha.weekday() >= 5:
                        continue
                    
                    # Evitar duplicados
                    if Asistencia.query.filter_by(empleado_id=empleado.id, fecha=fecha).first():
                        continue
                    
                    asistencia = Asistencia(
                        empleado_id=empleado.id,
                        fecha=fecha,
                        hora_entrada=datetime.strptime('08:00', '%H:%M').time(),
                        hora_salida=datetime.strptime('17:00', '%H:%M').time(),
                        presente=True,
                        fecha_creacion=datetime.utcnow()
                    )
                    db.session.add(asistencia)
                    contador_asistencias += 1
            
            db.session.commit()
            print(f"  ✓ {contador_asistencias} asistencias creadas")
        else:
            print("  ℹ️  Las asistencias ya existen")
        
        # ==================== VACACIONES ====================
        print("🏖️  Creando vacaciones...")
        
        vacaciones_existentes = Vacacion.query.count()
        if vacaciones_existentes == 0:
            empleados = Empleado.query.all()
            año_actual = date.today().year
            
            for empleado in empleados:
                vacacion = Vacacion(
                    empleado_id=empleado.id,
                    año=año_actual,
                    dias_disponibles=15,
                    dias_tomados=0,
                    dias_pendientes=15,
                    estado=EstadoVacacionEnum.PENDIENTE,
                    fecha_creacion=datetime.utcnow()
                )
                db.session.add(vacacion)
            
            db.session.commit()
            print(f"  ✓ Vacaciones creadas para {len(empleados)} empleados")
        else:
            print("  ℹ️  Las vacaciones ya existen")
        
        # ==================== RESUMEN ====================
        print("\n" + "="*50)
        print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("="*50)
        print("\n📊 Estadísticas:")
        print(f"  • Usuarios: {Usuario.query.count()}")
        print(f"  • Cargos: {Cargo.query.count()}")
        print(f"  • Empleados: {Empleado.query.count()}")
        print(f"  • Asistencias: {Asistencia.query.count()}")
        print(f"  • Vacaciones: {Vacacion.query.count()}")
        
        print("\n🔐 Usuarios de prueba:")
        print("  • Usuario: admin")
        print("  • Contraseña: admin123")
        print("  • Rol: RRHH")
        print("\n  • Usuario: asistente")
        print("  • Contraseña: asistente123")
        print("  • Rol: Asistente RRHH")
        
        print("\n🚀 Ejecuta: python run.py")
        print("📱 Accede: http://localhost:5000")
        print("\n")

if __name__ == '__main__':
    init_database()
