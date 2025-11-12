"""
Tests unitarios para flujo de despidos.
Valida cálculos de indemnización, aguinaldo, vacaciones y liquidación.
"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from app import create_app
from app.models import db, Empleado, Despido, Liquidacion, Cargo, Usuario, RoleEnum

@pytest.fixture
def app():
    """Crea aplicación Flask para testing con BD en memoria."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente HTTP para testing."""
    return app.test_client()

@pytest.fixture
def usuario_rrhh(app):
    """Usuario RRHH para testing."""
    with app.app_context():
        usuario = Usuario(
            nombre_usuario='rrhh_test',
            email='rrhh@test.com',
            nombre_completo='RRHH Test',
            rol=RoleEnum.RRHH
        )
        usuario.set_password('password123')
        db.session.add(usuario)
        db.session.commit()
        return usuario

@pytest.fixture
def cargo_test(app):
    """Cargo de prueba."""
    with app.app_context():
        cargo = Cargo(nombre='Gerente', descripcion='Gerente General')
        db.session.add(cargo)
        db.session.commit()
        return cargo

@pytest.fixture
def empleado_3_años(app, cargo_test):
    """Empleado con 3 años de antigüedad."""
    with app.app_context():
        fecha_inicio = date.today() - timedelta(days=365*3)
        empleado = Empleado(
            nombre='Juan Pérez',
            cedula='12345678',
            email='juan@test.com',
            salario_base=Decimal('2000000'),
            cargo_id=cargo_test.id,
            fecha_contratacion=fecha_inicio,
            estado='activo'
        )
        db.session.add(empleado)
        db.session.commit()
        return empleado

@pytest.fixture
def empleado_10_años(app, cargo_test):
    """Empleado con 10 años de antigüedad."""
    with app.app_context():
        fecha_inicio = date.today() - timedelta(days=365*10)
        empleado = Empleado(
            nombre='María García',
            cedula='87654321',
            email='maria@test.com',
            salario_base=Decimal('3500000'),
            cargo_id=cargo_test.id,
            fecha_contratacion=fecha_inicio,
            estado='activo'
        )
        db.session.add(empleado)
        db.session.commit()
        return empleado

# ==================== TESTS DE CÁLCULOS ====================

def test_calcular_antiguedad_años(app, empleado_3_años):
    """Verifica cálculo de antigüedad en años."""
    with app.app_context():
        from app.routes.rrhh import calcular_antiguedad_años
        
        años = calcular_antiguedad_años(
            empleado_3_años.fecha_contratacion,
            date.today()
        )
        
        assert años >= 3, f"Antigüedad debe ser >= 3, obtuvo {años}"

def test_calcular_indemnizacion_justificado(app):
    """Despido justificado retorna 0 indemnización."""
    with app.app_context():
        from app.routes.rrhh import calcular_indemnizacion
        
        monto = calcular_indemnizacion(
            salario_base=2000000,
            tipo_despido='justificado',
            antiguedad_años=5
        )
        
        assert monto == Decimal('0'), f"Indemnización justificado debe ser 0, obtuvo {monto}"

def test_calcular_indemnizacion_injustificado_1_año(app):
    """Despido injustificado con 1 año retorna 2 meses."""
    with app.app_context():
        from app.routes.rrhh import calcular_indemnizacion
        
        salario = Decimal('2000000')
        monto = calcular_indemnizacion(
            salario_base=salario,
            tipo_despido='injustificado',
            antiguedad_años=1
        )
        
        # 1 mes + 1 año = 2 meses
        esperado = Decimal('4000000')
        assert monto == esperado, f"Esperado {esperado}, obtuvo {monto}"

def test_calcular_indemnizacion_injustificado_5_años(app):
    """Despido injustificado con 5 años retorna 6 meses."""
    with app.app_context():
        from app.routes.rrhh import calcular_indemnizacion
        
        salario = Decimal('2000000')
        monto = calcular_indemnizacion(
            salario_base=salario,
            tipo_despido='injustificado',
            antiguedad_años=5
        )
        
        # 1 mes + 5 años = 6 meses
        esperado = Decimal('12000000')
        assert monto == esperado, f"Esperado {esperado}, obtuvo {monto}"

def test_calcular_indemnizacion_injustificado_cap_12(app):
    """Despido injustificado con 15 años capea a 12 meses."""
    with app.app_context():
        from app.routes.rrhh import calcular_indemnizacion
        
        salario = Decimal('2000000')
        monto = calcular_indemnizacion(
            salario_base=salario,
            tipo_despido='injustificado',
            antiguedad_años=15
        )
        
        # 1 + 15 = 16, pero capeado a 12
        esperado = Decimal('24000000')
        assert monto == esperado, f"Máximo debe ser 12 meses, obtuvo {monto/salario}"

def test_calcular_aguinaldo_proporcional_julio(app):
    """Aguinaldo en julio (7 meses trabajados)."""
    with app.app_context():
        from app.routes.rrhh import calcular_aguinaldo_proporcional
        
        salario = Decimal('2000000')
        # Simular despido en julio
        fecha_despido = date(date.today().year, 7, 31)
        
        aguinaldo = calcular_aguinaldo_proporcional(salario, fecha_despido)
        
        # 7 meses / 12 × 2,000,000
        # Aprox 1,166,666.67
        assert aguinaldo > Decimal('1100000'), f"Aguinaldo muy bajo: {aguinaldo}"
        assert aguinaldo < Decimal('1250000'), f"Aguinaldo muy alto: {aguinaldo}"

def test_calcular_aguinaldo_proporcional_diciembre(app):
    """Aguinaldo en diciembre debe ser casi 1 mes completo."""
    with app.app_context():
        from app.routes.rrhh import calcular_aguinaldo_proporcional
        
        salario = Decimal('2000000')
        # Despido en fin de año
        fecha_despido = date(date.today().year, 12, 31)
        
        aguinaldo = calcular_aguinaldo_proporcional(salario, fecha_despido)
        
        # 12 meses / 12 × 2,000,000 ≈ 2,000,000
        assert aguinaldo >= Decimal('1900000'), f"Aguinaldo debe ser cercano a 1 mes, obtuvo {aguinaldo}"

def test_calcular_aportes_ips(app):
    """Aportes IPS: 9% del monto."""
    with app.app_context():
        from app.routes.rrhh import calcular_aportes_ips_despido
        
        monto = Decimal('1000000')
        aportes = calcular_aportes_ips_despido(monto)
        
        # 9% de 1,000,000 = 90,000
        esperado = Decimal('90000')
        assert aportes == esperado, f"Esperado {esperado}, obtuvo {aportes}"

# ==================== TESTS DE FLUJO COMPLETO ====================

def test_generar_liquidacion_despido_justificado(app, usuario_rrhh, empleado_3_años):
    """Genera liquidación por despido justificado."""
    with app.app_context():
        from app.routes.rrhh import generar_liquidacion_despido
        
        # Simular login
        with app.test_request_context():
            from flask_login import login_user
            login_user(usuario_rrhh)
            
            resultado = generar_liquidacion_despido(
                empleado_3_años.id,
                'justificado',
                'ineptitud',
                'No cumple requisitos técnicos'
            )
        
        assert resultado is not None, "Resultado debe ser no nulo"
        assert resultado['indemnizacion'] == Decimal('0'), "Justificado debe tener 0 indemnización"
        assert resultado['aguinaldo'] > 0, "Aguinaldo debe ser > 0"
        assert resultado['vacaciones'] > 0, "Vacaciones debe ser > 0"
        assert resultado['aportes_ips'] > 0, "Aportes IPS debe ser > 0"
        assert resultado['total_liquido'] > 0, "Total neto debe ser > 0"
        
        # Verificar que se crearon registros en BD
        despido = Despido.query.filter_by(empleado_id=empleado_3_años.id).first()
        assert despido is not None, "Debe existir registro de Despido"
        assert despido.tipo == 'justificado'
        assert despido.causal == 'ineptitud'
        
        liquidacion = Liquidacion.query.filter_by(despido_id=despido.id).first()
        assert liquidacion is not None, "Debe existir registro de Liquidación"
        assert liquidacion.despido_id == despido.id

def test_generar_liquidacion_despido_injustificado(app, usuario_rrhh, empleado_10_años):
    """Genera liquidación por despido injustificado."""
    with app.app_context():
        from app.routes.rrhh import generar_liquidacion_despido
        
        with app.test_request_context():
            from flask_login import login_user
            login_user(usuario_rrhh)
            
            resultado = generar_liquidacion_despido(
                empleado_10_años.id,
                'injustificado',
                None,
                'Despido sin causa'
            )
        
        assert resultado is not None
        assert resultado['indemnizacion'] > 0, "Injustificado debe tener indemnización > 0"
        
        # 10 años: 1 + 10 = 11 meses (debajo del cap de 12)
        expected_meses = 11
        expected_indemnizacion = Decimal(expected_meses) * Decimal('3500000')
        assert resultado['indemnizacion'] == expected_indemnizacion, \
            f"Indemnización debe ser {expected_meses} meses"

def test_liquidacion_descuento_ips_sobre_total(app, usuario_rrhh, empleado_3_años):
    """Verifica que IPS se descuenta del total (indemnización + aguinaldo + vacaciones)."""
    with app.app_context():
        from app.routes.rrhh import generar_liquidacion_despido
        
        with app.test_request_context():
            from flask_login import login_user
            login_user(usuario_rrhh)
            
            resultado = generar_liquidacion_despido(
                empleado_3_años.id,
                'injustificado',
                None,
                'Test'
            )
        
        subtotal = resultado['indemnizacion'] + resultado['aguinaldo'] + resultado['vacaciones']
        aportes_calculados = subtotal * Decimal('0.09')
        neto_esperado = subtotal - aportes_calculados
        
        assert abs(resultado['total_liquido'] - neto_esperado) < Decimal('1'), \
            f"Neto debe ser subtotal - IPS"

# ==================== TESTS INTEGRACION ====================

def test_ruta_registrar_despido_get(client, usuario_rrhh):
    """GET /registrar_despido retorna formulario."""
    with client:
        client.post('/auth/login', data={
            'nombre_usuario': usuario_rrhh.nombre_usuario,
            'password': 'password123'
        })
        
        response = client.get('/rrhh/registrar_despido')
        assert response.status_code == 200
        assert b'Registrar Despido' in response.data

def test_ruta_liquidacion_despido_view(client, usuario_rrhh, empleado_3_años, app):
    """GET /liquidacion_despido/<id> muestra detalles."""
    with app.app_context():
        from app.routes.rrhh import generar_liquidacion_despido
        
        with app.test_request_context():
            from flask_login import login_user
            login_user(usuario_rrhh)
            
            resultado = generar_liquidacion_despido(
                empleado_3_años.id,
                'injustificado',
                None,
                'Test'
            )
            liquidacion_id = resultado['liquidacion_obj'].id
    
    with client:
        client.post('/auth/login', data={
            'nombre_usuario': usuario_rrhh.nombre_usuario,
            'password': 'password123'
        })
        
        response = client.get(f'/rrhh/liquidacion_despido/{liquidacion_id}')
        assert response.status_code == 200
        assert b'Liquidaci' in response.data or b'liquidaci' in response.data.lower()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
