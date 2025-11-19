"""
Verificar si el anticipo ID 7 fue descontado correctamente en la liquidación
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Cargar variables de entorno
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL no encontrado en .env")
    sys.exit(1)

print("="*80)
print("🔍 VERIFICACIÓN: Anticipo ID 7 - Carlos Rodríguez")
print("="*80)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor(cursor_factory=RealDictCursor)

# 1. Información del anticipo
print("\n📋 INFORMACIÓN DEL ANTICIPO:")
print("-"*80)
cur.execute("""
    SELECT 
        a.id,
        e.codigo,
        e.nombre || ' ' || e.apellido as empleado,
        a.monto,
        a.fecha_solicitud,
        a.fecha_aprobacion,
        a.aprobado,
        a.aplicado,
        a.fecha_aplicacion,
        TO_CHAR(a.fecha_aprobacion, 'YYYY-MM') as periodo
    FROM anticipos a
    JOIN empleados e ON e.id = a.empleado_id
    WHERE a.id = 7
""")
anticipo = cur.fetchone()

if anticipo:
    print(f"ID:                {anticipo['id']}")
    print(f"Empleado:          {anticipo['codigo']} - {anticipo['empleado']}")
    print(f"Monto:             ₲{anticipo['monto']:,.0f}")
    print(f"Fecha Aprobación:  {anticipo['fecha_aprobacion']}")
    print(f"Período:           {anticipo['periodo']}")
    print(f"Aplicado:          {'✅ SÍ' if anticipo['aplicado'] else '❌ NO'}")
    if anticipo['fecha_aplicacion']:
        print(f"Fecha Aplicación:  {anticipo['fecha_aplicacion']}")
    
    periodo = anticipo['periodo']
    empleado_id = None
    
    # Obtener empleado_id
    cur.execute("SELECT empleado_id FROM anticipos WHERE id = 7")
    result = cur.fetchone()
    empleado_id = result['empleado_id']
    
    # 2. Liquidación del período
    print(f"\n💵 LIQUIDACIÓN DEL PERÍODO {periodo}:")
    print("-"*80)
    cur.execute("""
        SELECT 
            l.id,
            l.periodo,
            l.salario_base,
            l.ingresos_extras,
            l.bonificacion_familiar,
            l.descuentos,
            l.aporte_ips,
            l.salario_neto,
            l.dias_trabajados
        FROM liquidaciones l
        WHERE l.empleado_id = %s AND l.periodo = %s
    """, (empleado_id, periodo))
    
    liquidacion = cur.fetchone()
    
    if liquidacion:
        print(f"ID Liquidación:         {liquidacion['id']}")
        print(f"Salario Base:           ₲{liquidacion['salario_base']:,.2f}")
        print(f"Ingresos Extras:        ₲{liquidacion['ingresos_extras']:,.2f}")
        print(f"Bonificación Familiar:  ₲{liquidacion['bonificacion_familiar']:,.2f}")
        print(f"DESCUENTOS:             ₲{liquidacion['descuentos']:,.2f}")
        print(f"Aporte IPS:             ₲{liquidacion['aporte_ips']:,.2f}")
        print(f"SALARIO NETO:           ₲{liquidacion['salario_neto']:,.2f}")
        print(f"Días Trabajados:        {liquidacion['dias_trabajados']}")
        
        # 3. Verificación
        print(f"\n🎯 VERIFICACIÓN:")
        print("-"*80)
        
        # Calcular descuentos esperados
        cur.execute("""
            SELECT COALESCE(SUM(monto), 0) as descuentos_manuales
            FROM descuentos
            WHERE empleado_id = %s 
            AND mes = CAST(SPLIT_PART(%s, '-', 2) AS INT)
            AND año = CAST(SPLIT_PART(%s, '-', 1) AS INT)
        """, (empleado_id, periodo, periodo))
        desc_manuales = cur.fetchone()['descuentos_manuales']
        
        descuentos_esperados = float(desc_manuales) + float(anticipo['monto'])
        descuentos_reales = float(liquidacion['descuentos'])
        
        print(f"Descuentos manuales:    ₲{desc_manuales:,.2f}")
        print(f"Anticipo ID 7:          ₲{anticipo['monto']:,.2f}")
        print(f"ESPERADO:               ₲{descuentos_esperados:,.2f}")
        print(f"REAL (en liquidación):  ₲{descuentos_reales:,.2f}")
        
        if abs(descuentos_reales - descuentos_esperados) < 0.01:
            print(f"\n✅ CORRECTO: El anticipo FUE DESCONTADO correctamente")
        else:
            print(f"\n❌ ERROR: El anticipo NO fue descontado")
            print(f"   Diferencia: ₲{abs(descuentos_reales - descuentos_esperados):,.2f}")
    else:
        print(f"❌ No se encontró liquidación para {periodo}")
        
else:
    print("❌ No se encontró el anticipo ID 7")

# 4. Todos los anticipos del empleado
print(f"\n📊 TODOS LOS ANTICIPOS DEL EMPLEADO:")
print("-"*80)
cur.execute("""
    SELECT 
        a.id,
        a.monto,
        a.fecha_aprobacion,
        TO_CHAR(a.fecha_aprobacion, 'YYYY-MM') as periodo,
        a.aprobado,
        a.aplicado,
        a.fecha_aplicacion
    FROM anticipos a
    WHERE a.empleado_id = %s
    ORDER BY a.fecha_aprobacion DESC
""", (empleado_id,))

anticipos_todos = cur.fetchall()
for ant in anticipos_todos:
    estado = "✅ Aplicado" if ant['aplicado'] else "⏳ Pendiente"
    print(f"ID {ant['id']}: ₲{ant['monto']:,.0f} - {ant['periodo']} - {estado}")

cur.close()
conn.close()

print("="*80)
print("✅ Verificación completada")
print("="*80)
