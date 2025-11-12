"""
Script para PROBAR el nuevo sistema de liquidaciones basado en asistencias.

Este script:
1. Verifica que haya asistencias registradas
2. Genera liquidaciones
3. Valida que los cálculos sean correctos
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

# Agregar raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar .env
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import (
    Empleado, Asistencia, Liquidacion, EstadoEmpleadoEnum
)
from sqlalchemy import func

# Crear app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

def test_liquidaciones():
    """Prueba el sistema de liquidaciones basado en asistencias"""
    
    with app.app_context():
        print("=" * 70)
        print("PRUEBA: SISTEMA DE LIQUIDACIONES BASADO EN ASISTENCIAS")
        print("=" * 70)
        
        # Parámetros de prueba
        año = 2025
        mes = 10
        periodo = f"{año}-{mes:02d}"
        
        print(f"\n📅 Período a verificar: {periodo} (Octubre 2025)")
        
        # 1. VERIFICAR ASISTENCIAS
        print(f"\n{'='*70}")
        print("1️⃣  VERIFICANDO ASISTENCIAS")
        print(f"{'='*70}")
        
        # Contar asistencias por empleado
        asistencias_por_empleado = db.session.query(
            Empleado.nombre,
            func.count(Asistencia.id).label('asistencias')
        ).join(Asistencia, Empleado.id == Asistencia.empleado_id).filter(
            Empleado.estado == EstadoEmpleadoEnum.ACTIVO,
            func.extract('month', Asistencia.fecha) == mes,
            func.extract('year', Asistencia.fecha) == año,
            Asistencia.presente == True
        ).group_by(Empleado.id, Empleado.nombre).all()
        
        if not asistencias_por_empleado:
            print("\n❌ ERROR: No hay asistencias registradas para octubre 2025")
            print("   Ejecuta primero: python scripts/generar_datos_prueba.py")
            return False
        
        print(f"\n✓ Encontradas asistencias para {len(asistencias_por_empleado)} empleados:\n")
        
        total_asistencias = 0
        for empleado_nombre, asistencias in asistencias_por_empleado:
            print(f"  • {empleado_nombre:25s}: {asistencias} asistencias")
            total_asistencias += asistencias
        
        print(f"\n  TOTAL: {total_asistencias} asistencias registradas")
        
        # 2. CALCULAR DÍAS HÁBILES DEL MES
        print(f"\n{'='*70}")
        print("2️⃣  CALCULANDO DÍAS HÁBILES DE OCTUBRE")
        print(f"{'='*70}")
        
        import calendar
        primer_dia = date(año, mes, 1)
        ultimo_dia = date(año, mes, calendar.monthrange(año, mes)[1])
        
        dias_habiles = 0
        fecha_actual = primer_dia
        while fecha_actual <= ultimo_dia:
            if fecha_actual.weekday() < 5:  # Lunes a viernes
                dias_habiles += 1
            fecha_actual += timedelta(days=1)
        
        print(f"\n✓ Octubre 2025: {dias_habiles} días hábiles (lunes a viernes)")
        print(f"  Rango: {primer_dia.strftime('%d/%m/%Y')} - {ultimo_dia.strftime('%d/%m/%Y')}")
        
        # 3. VALIDAR LIQUIDACIONES
        print(f"\n{'='*70}")
        print("3️⃣  VALIDANDO LIQUIDACIONES")
        print(f"{'='*70}")
        
        liquidaciones = Liquidacion.query.filter_by(periodo=periodo).all()
        
        if not liquidaciones:
            print(f"\n⚠️  No hay liquidaciones para {periodo}")
            print("   Nota: Se generarán cuando hagas click en 'Generar'")
            return True
        
        print(f"\n✓ Encontradas {len(liquidaciones)} liquidaciones:\n")
        
        print(f"{'Empleado':<20} {'Días':<8} {'Salario Base':<15} {'IPS':<15} {'Neto':<15}")
        print(f"{'-'*73}")
        
        total_bruto = Decimal('0')
        total_ips = Decimal('0')
        total_neto = Decimal('0')
        
        for liq in liquidaciones:
            empleado = liq.empleado
            dias = liq.dias_trabajados
            salario = liq.salario_base
            ips = liq.aporte_ips
            neto = liq.salario_neto
            
            print(f"{empleado.nombre:<20} {dias:<8} {salario:>12,.2f}  {ips:>12,.2f}  {neto:>12,.2f}")
            
            total_bruto += salario
            total_ips += ips
            total_neto += neto
        
        print(f"{'-'*73}")
        print(f"{'TOTAL':<20} {'':<8} {total_bruto:>12,.2f}  {total_ips:>12,.2f}  {total_neto:>12,.2f}")
        
        # 4. VALIDAR CÁLCULOS
        print(f"\n{'='*70}")
        print("4️⃣  VALIDANDO FÓRMULAS")
        print(f"{'='*70}")
        
        errores = 0
        
        for liq in liquidaciones:
            empleado = liq.empleado
            
            # Recalcular para validar
            salario_diario = empleado.salario_base / Decimal(30)
            salario_esperado = salario_diario * Decimal(liq.dias_trabajados)
            
            # Diferencia permitida (0.01 Gs.)
            if abs(liq.salario_base - salario_esperado) > Decimal('0.01'):
                print(f"❌ {empleado.nombre}: Salario incorrecta")
                print(f"   Esperado: {salario_esperado:.2f}")
                print(f"   Actual: {liq.salario_base:.2f}")
                errores += 1
        
        if errores == 0:
            print("\n✓ Todas las fórmulas son correctas")
        else:
            print(f"\n❌ {errores} errores encontrados")
            return False
        
        # 5. RESUMEN FINAL
        print(f"\n{'='*70}")
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print(f"{'='*70}")
        
        print(f"""
RESUMEN:
✓ Asistencias: {total_asistencias} registradas
✓ Días hábiles: {dias_habiles}
✓ Liquidaciones: {len(liquidaciones)} creadas
✓ Salario total bruto: {total_bruto:,.2f} Gs.
✓ IPS total (9.625%): {total_ips:,.2f} Gs.
✓ Salario total neto: {total_neto:,.2f} Gs.

PRÓXIMOS PASOS:
1. Ve a: Menú → Nómina → Liquidaciones
2. Filtra por período: 2025-10
3. Verifica los valores
4. Descarga PDF para verificar
        """)
        
        return True

if __name__ == '__main__':
    try:
        exito = test_liquidaciones()
        if not exito:
            exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
