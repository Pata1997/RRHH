#!/usr/bin/env python
"""
Script de auditoría automática para detectar anticipos no descontados
Ejecutar: python scripts/auditoria_anticipos.py
"""
import os
import sys
from decimal import Decimal
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print('❌ ERROR: DATABASE_URL no encontrado en .env')
    sys.exit(1)

print("=" * 70)
print("🔍 AUDITORÍA: Anticipos No Descontados en Liquidaciones")
print("=" * 70)

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # =====================================================
    # QUERY #2: RESUMEN TOTAL DE PÉRDIDAS (MÁS IMPORTANTE)
    # =====================================================
    print("\n📊 RESUMEN TOTAL DE PÉRDIDAS:\n")
    
    cur.execute("""
        SELECT 
            COUNT(DISTINCT l.id) as liquidaciones_afectadas,
            COUNT(DISTINCT e.id) as empleados_afectados,
            COALESCE(SUM(a.monto), 0) as perdida_total_empresa
        FROM liquidaciones l
        JOIN empleados e ON e.id = l.empleado_id
        JOIN anticipos a ON (
            a.empleado_id = l.empleado_id
            AND a.aprobado = TRUE
            AND (a.aplicado = FALSE OR a.aplicado IS NULL)
            AND EXTRACT(YEAR FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 1) AS INT)
            AND EXTRACT(MONTH FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 2) AS INT)
        )
    """)
    
    result = cur.fetchone()
    liquidaciones_afectadas = result[0] or 0
    empleados_afectados = result[1] or 0
    perdida_total = Decimal(str(result[2] or 0))
    
    print(f"   Liquidaciones con anticipos no descontados: {liquidaciones_afectadas}")
    print(f"   Empleados afectados: {empleados_afectados}")
    print(f"   💰 PÉRDIDA TOTAL: ₲{perdida_total:,.0f}")
    
    if liquidaciones_afectadas == 0:
        print("\n✅ EXCELENTE: No hay anticipos sin descontar en liquidaciones anteriores")
        print("   El fix ya estaba funcionando o no había anticipos previos.")
    else:
        print(f"\n⚠️  ATENCIÓN: Se encontraron {liquidaciones_afectadas} liquidaciones con anticipos no descontados")
        print(f"   Pérdida económica: ₲{perdida_total:,.0f}")
    
    # =====================================================
    # QUERY #1: DETALLE POR EMPLEADO
    # =====================================================
    if liquidaciones_afectadas > 0:
        print("\n" + "=" * 70)
        print("📋 DETALLE POR EMPLEADO:")
        print("=" * 70 + "\n")
        
        cur.execute("""
            SELECT 
                e.codigo,
                e.nombre || ' ' || e.apellido as nombre_completo,
                l.periodo,
                l.salario_neto as salario_pagado,
                COALESCE(SUM(a.monto), 0) as anticipos_no_descontados
            FROM liquidaciones l
            JOIN empleados e ON e.id = l.empleado_id
            LEFT JOIN anticipos a ON (
                a.empleado_id = l.empleado_id
                AND a.aprobado = TRUE
                AND (a.aplicado = FALSE OR a.aplicado IS NULL)
                AND EXTRACT(YEAR FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 1) AS INT)
                AND EXTRACT(MONTH FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 2) AS INT)
            )
            WHERE a.id IS NOT NULL
            GROUP BY e.codigo, e.nombre, e.apellido, l.periodo, l.salario_neto, l.id
            ORDER BY l.periodo DESC, e.codigo
        """)
        
        rows = cur.fetchall()
        print(f"{'Código':<10} {'Nombre':<25} {'Período':<10} {'Anticipo No Descontado':>20}")
        print("-" * 70)
        
        for row in rows:
            codigo, nombre, periodo, salario, anticipo = row
            print(f"{codigo:<10} {nombre:<25} {periodo:<10} ₲{Decimal(str(anticipo)):>18,.0f}")
    
    # =====================================================
    # QUERY #3: ANTICIPOS PENDIENTES ACTUALES
    # =====================================================
    print("\n" + "=" * 70)
    print("📌 ANTICIPOS PENDIENTES DE APLICAR (ACTUALES):")
    print("=" * 70 + "\n")
    
    cur.execute("""
        SELECT 
            e.codigo,
            e.nombre || ' ' || e.apellido as nombre_completo,
            a.monto as anticipo_pendiente,
            a.fecha_aprobacion,
            TO_CHAR(a.fecha_aprobacion, 'YYYY-MM') as periodo_a_descontar,
            CASE 
                WHEN l.id IS NOT NULL THEN 'YA LIQUIDADO (no descontado)'
                ELSE 'Pendiente de liquidación'
            END as estado
        FROM anticipos a
        JOIN empleados e ON e.id = a.empleado_id
        LEFT JOIN liquidaciones l ON (
            l.empleado_id = a.empleado_id
            AND l.periodo = TO_CHAR(a.fecha_aprobacion, 'YYYY-MM')
        )
        WHERE a.aprobado = TRUE
          AND (a.aplicado = FALSE OR a.aplicado IS NULL)
        ORDER BY a.fecha_aprobacion DESC
    """)
    
    anticipos_pendientes = cur.fetchall()
    
    if len(anticipos_pendientes) == 0:
        print("✅ No hay anticipos pendientes de aplicar")
    else:
        print(f"{'Código':<10} {'Nombre':<25} {'Monto':>15} {'Período':<10} {'Estado':<30}")
        print("-" * 95)
        
        total_pendiente = Decimal('0')
        for row in anticipos_pendientes:
            codigo, nombre, monto, fecha, periodo, estado = row
            monto_dec = Decimal(str(monto))
            total_pendiente += monto_dec
            print(f"{codigo:<10} {nombre:<25} ₲{monto_dec:>12,.0f} {periodo:<10} {estado:<30}")
        
        print("-" * 95)
        print(f"{'TOTAL PENDIENTE:':>50} ₲{total_pendiente:>12,.0f}")
    
    # =====================================================
    # CONCLUSIÓN Y RECOMENDACIONES
    # =====================================================
    print("\n" + "=" * 70)
    print("🎯 CONCLUSIÓN Y RECOMENDACIONES:")
    print("=" * 70 + "\n")
    
    if liquidaciones_afectadas == 0 and len(anticipos_pendientes) == 0:
        print("✅ Sistema está limpio:")
        print("   - No hay liquidaciones anteriores con anticipos sin descontar")
        print("   - No hay anticipos pendientes actuales")
        print("   - El fix está listo para funcionar correctamente")
        print("\n👉 ACCIÓN: Puedes generar liquidaciones con confianza")
    
    elif liquidaciones_afectadas > 0 and len(anticipos_pendientes) == 0:
        print("⚠️  Hay pérdidas históricas pero ya no hay anticipos pendientes:")
        print(f"   - Pérdida total: ₲{perdida_total:,.0f}")
        print(f"   - Liquidaciones afectadas: {liquidaciones_afectadas}")
        print(f"   - Empleados afectados: {empleados_afectados}")
        print("\n👉 ACCIÓN: Considera ajustar liquidaciones pasadas manualmente")
        print("   (Consultar con contabilidad)")
    
    elif liquidaciones_afectadas == 0 and len(anticipos_pendientes) > 0:
        print(f"⚠️  Hay {len(anticipos_pendientes)} anticipos pendientes:")
        print(f"   - Total: ₲{total_pendiente:,.0f}")
        print("\n👉 ACCIÓN: Al generar próxima liquidación, estos se descontarán automáticamente")
        print("   (El fix ya está aplicado)")
    
    else:
        print(f"🔴 SITUACIÓN CRÍTICA:")
        print(f"   - Pérdida histórica: ₲{perdida_total:,.0f}")
        print(f"   - Anticipos pendientes: {len(anticipos_pendientes)} (₲{total_pendiente:,.0f})")
        print("\n👉 ACCIONES:")
        print("   1. Revisar liquidaciones anteriores con contabilidad")
        print("   2. Generar nueva liquidación (con fix ya aplicado)")
        print("   3. Verificar que anticipos se descuenten correctamente")
    
    print("\n" + "=" * 70)
    print("✅ Auditoría completada")
    print("=" * 70)
    
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f"\n❌ ERROR de base de datos:")
    print(f"   {str(e)}")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ ERROR inesperado:")
    print(f"   {str(e)}")
    sys.exit(1)
