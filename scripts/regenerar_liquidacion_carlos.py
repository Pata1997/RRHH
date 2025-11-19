"""
Regenerar liquidación de Carlos Rodríguez (EMP003) para noviembre 2025
"""
import os
import sys

# Ajustar path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Liquidacion, Empleado, Anticipo
from datetime import date
from sqlalchemy import func
from decimal import Decimal

app = create_app()

with app.app_context():
    print("="*80)
    print("🔄 REGENERAR LIQUIDACIÓN: Carlos Rodríguez (EMP003) - 2025-11")
    print("="*80)
    
    # Buscar empleado
    empleado = Empleado.query.filter_by(codigo='EMP003').first()
    if not empleado:
        print("❌ No se encontró empleado EMP003")
        sys.exit(1)
    
    print(f"\n👤 Empleado: {empleado.nombre} {empleado.apellido}")
    print(f"   Salario base: ₲{empleado.salario_base:,.2f}")
    
    periodo = '2025-11'
    mes = 11
    año = 2025
    
    # 1. Verificar anticipos pendientes
    print(f"\n📋 ANTICIPOS PENDIENTES:")
    print("-"*80)
    anticipos = Anticipo.query.filter(
        Anticipo.empleado_id == empleado.id,
        func.extract('month', Anticipo.fecha_aprobacion) == mes,
        func.extract('year', Anticipo.fecha_aprobacion) == año,
        Anticipo.aprobado == True,
        Anticipo.aplicado == False
    ).all()
    
    total_anticipos = Decimal('0')
    for ant in anticipos:
        print(f"   Anticipo ID {ant.id}: ₲{ant.monto:,.0f} - {ant.fecha_aprobacion}")
        total_anticipos += Decimal(str(ant.monto))
    
    print(f"\n   TOTAL A DESCONTAR: ₲{total_anticipos:,.2f}")
    
    # 2. Eliminar liquidación existente
    liquidacion_vieja = Liquidacion.query.filter_by(
        empleado_id=empleado.id,
        periodo=periodo
    ).first()
    
    if liquidacion_vieja:
        print(f"\n🗑️  ELIMINANDO liquidación ID {liquidacion_vieja.id}")
        print(f"   Salario neto anterior: ₲{liquidacion_vieja.salario_neto:,.2f}")
        print(f"   Descuentos anteriores: ₲{liquidacion_vieja.descuentos:,.2f}")
        db.session.delete(liquidacion_vieja)
        db.session.commit()
        print("   ✅ Eliminada")
    
    # 3. Resetear anticipos a no aplicados (por si acaso)
    for ant in anticipos:
        ant.aplicado = False
        ant.fecha_aplicacion = None
    db.session.commit()
    print(f"\n🔄 Anticipos reseteados a NO APLICADOS")
    
    # 4. Crear nueva liquidación
    print(f"\n💰 GENERANDO NUEVA LIQUIDACIÓN:")
    print("-"*80)
    
    salario_base = Decimal(str(empleado.salario_base))
    ingresos_extras = Decimal('0')
    bonificacion = Decimal('0')
    descuentos_manuales = Decimal('40000')  # Ya existe según la auditoría
    aporte_ips = salario_base * Decimal('0.09625')
    
    # IMPORTANTE: Sumar anticipos a descuentos
    descuentos_totales = descuentos_manuales + total_anticipos
    
    salario_neto = salario_base + ingresos_extras + bonificacion - descuentos_totales - aporte_ips
    
    print(f"   Salario base:           ₲{salario_base:,.2f}")
    print(f"   Ingresos extras:        ₲{ingresos_extras:,.2f}")
    print(f"   Bonificación familiar:  ₲{bonificacion:,.2f}")
    print(f"   Descuentos manuales:    ₲{descuentos_manuales:,.2f}")
    print(f"   Anticipos del mes:      ₲{total_anticipos:,.2f}")
    print(f"   DESCUENTOS TOTALES:     ₲{descuentos_totales:,.2f}")
    print(f"   Aporte IPS (9.625%):    ₲{aporte_ips:,.2f}")
    print(f"   {'='*60}")
    print(f"   💵 SALARIO NETO:        ₲{salario_neto:,.2f}")
    print(f"   {'='*60}")
    
    nueva_liquidacion = Liquidacion(
        empleado_id=empleado.id,
        periodo=periodo,
        salario_base=salario_base,
        ingresos_extras=ingresos_extras,
        bonificacion_familiar=bonificacion,
        descuentos=descuentos_totales,
        aporte_ips=aporte_ips,
        salario_neto=salario_neto,
        dias_trabajados=30
    )
    
    db.session.add(nueva_liquidacion)
    
    # 5. Marcar anticipos como aplicados
    print(f"\n✅ MARCANDO ANTICIPOS COMO APLICADOS:")
    for ant in anticipos:
        ant.aplicado = True
        ant.fecha_aplicacion = date(año, mes, 1)
        print(f"   ✅ Anticipo ID {ant.id} marcado")
    
    db.session.commit()
    
    print(f"\n{'='*80}")
    print(f"✅ LIQUIDACIÓN REGENERADA CORRECTAMENTE")
    print(f"{'='*80}")
    print(f"\n📊 RESUMEN:")
    print(f"   ID Liquidación: {nueva_liquidacion.id}")
    print(f"   Anticipos aplicados: {len(anticipos)}")
    print(f"   Descuentos totales: ₲{descuentos_totales:,.2f}")
    print(f"   Salario neto: ₲{salario_neto:,.2f}")
    print(f"\n🎯 AHORA PUEDES:")
    print(f"   1. Ir a http://127.0.0.1:5000/rrhh/liquidaciones")
    print(f"   2. Buscar liquidación de Carlos Rodríguez - 2025-11")
    print(f"   3. Verificar que descuentos = ₲{descuentos_totales:,.2f}")
    print(f"   4. Verificar en perfil que anticipo ID 7 esté APLICADO")
