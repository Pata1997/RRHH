#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para migrar/crear tablas directamente en PostgreSQL
(Evita el fallback a SQLite)

Uso:
    python migrate_to_postgres.py
"""

import os
import sys
from datetime import datetime, date, timedelta
from decimal import Decimal
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Obtener DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    print("❌ ERROR: DATABASE_URL no está en .env")
    print("   Debe ser: postgresql://rrhh_user:123456@localhost:5432/rrhh_db")
    sys.exit(1)

# Agregar directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar DESPUÉS de cargar .env
os.environ['SQLALCHEMY_DATABASE_URI'] = database_url

from app import create_app, db
from app.models import (
    Usuario, Cargo, Empleado, Asistencia, Permiso, 
    Sancion, Liquidacion, Vacacion, RoleEnum, EstadoEmpleadoEnum,
    EstadoPermisoEnum, EstadoVacacionEnum
)

def migrate_to_postgres():
    """Migra todas las tablas a PostgreSQL"""
    
    print("=" * 60)
    print("🐘 MIGRAR TABLAS A PostgreSQL")
    print("=" * 60)
    print(f"\n🔗 DATABASE_URL: {database_url}")
    
    # Crear app con configuración de producción (usa DATABASE_URL sin fallback)
    app = create_app('production')
    
    with app.app_context():
        try:
            print("\n📦 Creando tablas en PostgreSQL...")
            db.create_all()
            print("✓ Tablas creadas exitosamente")
            
            # ==================== USUARIOS ====================
            print("\n👤 Creando usuarios...")
            
            usuario_admin = Usuario.query.filter_by(nombre_usuario='admin').first()
            if not usuario_admin:
                usuario_admin = Usuario(
                    nombre_usuario='admin',
                    email='admin@cooperativa.com',
                    nombre_completo='Administrador del Sistema',
                    rol=RoleEnum.RRHH,
                    activo=True
                )
                usuario_admin.set_password('admin123')
                db.session.add(usuario_admin)
                print("  ✓ Usuario admin creado")
            else:
                print("  ℹ️  Usuario admin ya existe")
            
            usuario_asistente = Usuario.query.filter_by(nombre_usuario='asistente').first()
            if not usuario_asistente:
                usuario_asistente = Usuario(
                    nombre_usuario='asistente',
                    email='asistente@cooperativa.com',
                    nombre_completo='Asistente de RRHH',
                    rol=RoleEnum.ASISTENTE_RRHH,
                    activo=True
                )
                usuario_asistente.set_password('asistente123')
                db.session.add(usuario_asistente)
                print("  ✓ Usuario asistente creado")
            else:
                print("  ℹ️  Usuario asistente ya existe")
            
            db.session.commit()
            
            # ==================== CARGOS ====================
            print("\n💼 Creando cargos...")
            
            if Cargo.query.count() == 0:
                cargos_datos = [
                    {'nombre': 'Gerente General', 'descripcion': 'Gerente General', 'salario_base': Decimal('5000000')},
                    {'nombre': 'Contador', 'descripcion': 'Contador', 'salario_base': Decimal('3000000')},
                    {'nombre': 'Recursos Humanos', 'descripcion': 'RRHH', 'salario_base': Decimal('2500000')},
                    {'nombre': 'Operario', 'descripcion': 'Operario', 'salario_base': Decimal('1500000')},
                    {'nombre': 'Asistente Administrativo', 'descripcion': 'Asistente', 'salario_base': Decimal('1200000')},
                    {'nombre': 'Supervisor', 'descripcion': 'Supervisor', 'salario_base': Decimal('2000000')},
                ]
                
                for cargo_data in cargos_datos:
                    cargo = Cargo(**cargo_data)
                    db.session.add(cargo)
                
                db.session.commit()
                print(f"  ✓ {len(cargos_datos)} cargos creados")
            else:
                print(f"  ℹ️  Los cargos ya existen ({Cargo.query.count()})")
            
            # ==================== EMPLEADOS ====================
            print("\n👥 Creando empleados...")
            
            if Empleado.query.count() == 0:
                gerente = Cargo.query.filter_by(nombre='Gerente General').first()
                contador = Cargo.query.filter_by(nombre='Contador').first()
                asistente = Cargo.query.filter_by(nombre='Asistente Administrativo').first()
                
                empleados_datos = [
                    {
                        'codigo': 'EMP001',
                        'nombre': 'Juan',
                        'apellido': 'García',
                        'ci': '1234567',
                        'email': 'juan@cooperativa.com',
                        'cargo_id': gerente.id,
                        'salario_base': Decimal('5000000'),
                        'fecha_ingreso': date(2020, 1, 15),
                        'estado': EstadoEmpleadoEnum.ACTIVO
                    },
                    {
                        'codigo': 'EMP002',
                        'nombre': 'María',
                        'apellido': 'López',
                        'ci': '1234568',
                        'email': 'maria@cooperativa.com',
                        'cargo_id': contador.id,
                        'salario_base': Decimal('3000000'),
                        'fecha_ingreso': date(2021, 3, 20),
                        'estado': EstadoEmpleadoEnum.ACTIVO
                    },
                    {
                        'codigo': 'EMP003',
                        'nombre': 'Carlos',
                        'apellido': 'Rodríguez',
                        'ci': '1234569',
                        'email': 'carlos@cooperativa.com',
                        'cargo_id': asistente.id,
                        'salario_base': Decimal('1200000'),
                        'fecha_ingreso': date(2022, 6, 10),
                        'estado': EstadoEmpleadoEnum.ACTIVO
                    },
                    {
                        'codigo': 'EMP004',
                        'nombre': 'Ana',
                        'apellido': 'Martínez',
                        'ci': '1234570',
                        'email': 'ana@cooperativa.com',
                        'cargo_id': asistente.id,
                        'salario_base': Decimal('1200000'),
                        'fecha_ingreso': date(2022, 9, 15),
                        'estado': EstadoEmpleadoEnum.ACTIVO
                    },
                    {
                        'codigo': 'EMP005',
                        'nombre': 'Pedro',
                        'apellido': 'González',
                        'ci': '1234571',
                        'email': 'pedro@cooperativa.com',
                        'cargo_id': asistente.id,
                        'salario_base': Decimal('1200000'),
                        'fecha_ingreso': date(2023, 1, 10),
                        'estado': EstadoEmpleadoEnum.ACTIVO
                    },
                ]
                
                for emp_data in empleados_datos:
                    empleado = Empleado(**emp_data)
                    db.session.add(empleado)
                
                db.session.commit()
                print(f"  ✓ {len(empleados_datos)} empleados creados")
            else:
                print(f"  ℹ️  Los empleados ya existen ({Empleado.query.count()})")
            
            # ==================== ASISTENCIAS ====================
            print("\n📅 Creando asistencias...")
            
            if Asistencia.query.count() == 0:
                empleados = Empleado.query.all()
                fecha_inicio = date.today() - timedelta(days=30)
                contador_asistencias = 0
                
                for empleado in empleados:
                    fecha_actual = fecha_inicio
                    while fecha_actual <= date.today():
                        # Saltar fines de semana
                        if fecha_actual.weekday() < 5:
                            asistencia = Asistencia(
                                empleado_id=empleado.id,
                                fecha=fecha_actual,
                                hora_entrada=datetime.strptime('08:00', '%H:%M').time(),
                                hora_salida=datetime.strptime('17:00', '%H:%M').time()
                            )
                            db.session.add(asistencia)
                            contador_asistencias += 1
                        
                        fecha_actual += timedelta(days=1)
                
                db.session.commit()
                print(f"  ✓ {contador_asistencias} asistencias creadas")
            else:
                print(f"  ℹ️  Las asistencias ya existen ({Asistencia.query.count()})")
            
            # ==================== VACACIONES ====================
            print("\n🏖️  Creando vacaciones...")
            
            if Vacacion.query.count() == 0:
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
                print(f"  ℹ️  Las vacaciones ya existen ({Vacacion.query.count()})")
            
            # ==================== RESUMEN ====================
            print("\n" + "=" * 60)
            print("✅ MIGRACIÓN A PostgreSQL COMPLETADA")
            print("=" * 60)
            print(f"\n📊 Estadísticas:")
            print(f"  • Usuarios: {Usuario.query.count()}")
            print(f"  • Cargos: {Cargo.query.count()}")
            print(f"  • Empleados: {Empleado.query.count()}")
            print(f"  • Asistencias: {Asistencia.query.count()}")
            print(f"  • Vacaciones: {Vacacion.query.count()}")
            
            print(f"\n🚀 Próximos pasos:")
            print(f"  1. Verificar tablas en pgAdmin (Database > rrhh_db > Schemas > public > Tables)")
            print(f"  2. python run.py")
            print(f"  3. http://localhost:5000")
            
            return True
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = migrate_to_postgres()
    sys.exit(0 if success else 1)
