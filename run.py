import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import Usuario, Cargo, Empleado, RoleEnum, EstadoEmpleadoEnum
from datetime import datetime, date
from decimal import Decimal

load_dotenv()

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Usuario': Usuario,
        'Cargo': Cargo,
        'Empleado': Empleado,
        'RoleEnum': RoleEnum,
        'EstadoEmpleadoEnum': EstadoEmpleadoEnum
    }

@app.cli.command()
def init_db():
    """Inicializa la base de datos con datos de prueba"""
    # Crear tablas
    db.create_all()
    
    # Crear usuario admin
    if Usuario.query.filter_by(nombre_usuario='admin').first() is None:
        admin = Usuario(
            nombre_usuario='admin',
            email='admin@cooperativa.com',
            nombre_completo='Administrador del Sistema',
            rol=RoleEnum.ADMIN,
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Crear usuario asistente
    if Usuario.query.filter_by(nombre_usuario='asistente').first() is None:
        asistente = Usuario(
            nombre_usuario='asistente',
            email='asistente@cooperativa.com',
            nombre_completo='Asistente de RRHH',
            rol=RoleEnum.ASISTENTE_RRHH,
            activo=True
        )
        asistente.set_password('asistente123')
        db.session.add(asistente)
    
    # Crear cargos de ejemplo
    if Cargo.query.count() == 0:
        cargos_datos = [
            {'nombre': 'Gerente General', 'descripcion': 'Gerente General de la Cooperativa', 'salario_base': Decimal('5000000')},
            {'nombre': 'Contador', 'descripcion': 'Contador responsable de finanzas', 'salario_base': Decimal('3000000')},
            {'nombre': 'Recursos Humanos', 'descripcion': 'Especialista en RRHH', 'salario_base': Decimal('2500000')},
            {'nombre': 'Operario', 'descripcion': 'Operario de producción', 'salario_base': Decimal('1500000')},
            {'nombre': 'Asistente Administrativo', 'descripcion': 'Asistente de tareas administrativas', 'salario_base': Decimal('1200000')},
        ]
        
        for cargo_data in cargos_datos:
            cargo = Cargo(**cargo_data)
            db.session.add(cargo)
    
    # Crear empleados de ejemplo
    if Empleado.query.count() == 0:
        # Obtener cargos
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
        ]
        
        for emp_data in empleados_datos:
            empleado = Empleado(**emp_data)
            db.session.add(empleado)
    
    db.session.commit()
    print('✓ Base de datos inicializada correctamente')
    print('  Usuario admin: admin / admin123')
    print('  Usuario asistente: asistente / asistente123')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
