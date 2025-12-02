"""
Script para generar datos de prueba realistas.

ACTUALIZADO PARA PROBAR DETECCIÓN RETROACTIVA DE AUSENCIAS:
- Crea asistencias hasta hace 5 días
- Deja vacíos los últimos 4 días hábiles
- Al acceder al dashboard, debería detectarlos y crear ausencias pendientes

Ejecutar: python scripts/generar_datos_prueba.py
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal
import calendar

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno ANTES de importar app
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Empleado, Asistencia, Descuento, Sancion, EstadoEmpleadoEnum

# Crear app con configuración de development (usa DATABASE_URL del .env)
app = create_app(os.environ.get('FLASK_ENV', 'development'))

def generar_datos_prueba():
    """Genera datos realistas de prueba - ACTUALIZADO para probar detección retroactiva"""
    
    with app.app_context():
        print("=" * 60)
        print("GENERADOR DE DATOS DE PRUEBA")
        print("SIMULA SISTEMA APAGADO - PRUEBA DETECCIÓN RETROACTIVA")
        print("=" * 60)
        
        # Obtener los empleados activos
        empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
        
        if len(empleados) < 1:
            print(f"\n❌ ERROR: No hay empleados activos.")
            return False
        
        print(f"\n✓ Encontrados {len(empleados)} empleados activos:")
        for emp in empleados:
            print(f"  - {emp.nombre_completo} (ID: {emp.id})")
        
        # ============================================
        # PASO 1: BORRAR ASISTENCIAS DE LOS ÚLTIMOS 4 DÍAS HÁBILES
        # ============================================
        print(f"\n🗑️  PASO 1: Borrando asistencias de los últimos 4 días hábiles...")
        print(f"   (Simula que el sistema estuvo apagado)")
        
        hoy = date.today()
        dias_a_borrar = []
        fecha_check = hoy - timedelta(days=1)
        
        # Buscar los últimos 4 días hábiles
        while len(dias_a_borrar) < 4:
            if fecha_check.weekday() < 5:  # Solo lunes a viernes
                dias_a_borrar.append(fecha_check)
            fecha_check -= timedelta(days=1)
        
        dias_a_borrar.reverse()  # Ordenar cronológicamente
        
        print(f"   Días a borrar:")
        for dia in dias_a_borrar:
            print(f"     - {dia.strftime('%d/%m/%Y - %A')}")
        
        borradas = 0
        for dia in dias_a_borrar:
            eliminadas = Asistencia.query.filter_by(fecha=dia).delete()
            borradas += eliminadas
        
        db.session.commit()
        print(f"   ✓ {borradas} asistencias eliminadas")
        
        # ============================================
        # PASO 2: CREAR ASISTENCIAS HASTA HACE 5 DÍAS
        # ============================================
        print(f"\n📝 PASO 2: Creando asistencias hasta hace 5 días hábiles...")
        
        # Calcular fecha límite (hace 5 días hábiles)
        fecha_limite = hoy - timedelta(days=7)  # Empezar desde hace una semana
        dias_creados = []
        fecha_check = fecha_limite
        
        # Buscar hasta 10 días hábiles atrás
        while len(dias_creados) < 10 and fecha_check < (hoy - timedelta(days=4)):
            if fecha_check.weekday() < 5:  # Solo lunes a viernes
                dias_creados.append(fecha_check)
            fecha_check += timedelta(days=1)
        
        print(f"   Creando asistencias para {len(dias_creados)} días:")
        for dia in dias_creados:
            print(f"     - {dia.strftime('%d/%m/%Y - %A')}")
        
        contador_asistencias = 0
        for empleado in empleados:
            for día in dias_creados:
                # Verificar si ya existe
                existe = Asistencia.query.filter_by(
                    empleado_id=empleado.id,
                    fecha=día
                ).first()
                
                if not existe:
                    asistencia = Asistencia(
                        empleado_id=empleado.id,
                        fecha=día,
                        hora_entrada=datetime.strptime("08:00", "%H:%M").time(),
                        hora_salida=datetime.strptime("17:00", "%H:%M").time(),
                        presente=True,
                        observaciones="Presente - Asistencia normal"
                    )
                    db.session.add(asistencia)
                    contador_asistencias += 1
        
        db.session.commit()
        print(f"   ✓ {contador_asistencias} asistencias creadas")
        
        # ============================================
        # RESUMEN FINAL
        # ============================================
        print(f"\n" + "=" * 60)
        print("✅ DATOS DE PRUEBA GENERADOS")
        print("=" * 60)
        
        print(f"""
RESUMEN:
✓ Eliminadas: {borradas} asistencias de los últimos 4 días hábiles
✓ Creadas: {contador_asistencias} asistencias de días anteriores
✓ Empleados procesados: {len(empleados)}

📌 DÍAS SIN ASISTENCIAS (simulan sistema apagado):
""")
        for dia in dias_a_borrar:
            print(f"   ❌ {dia.strftime('%d/%m/%Y - %A')} - SIN REGISTROS")
        
        print(f"""
🎯 PRÓXIMOS PASOS PARA PROBAR LA DETECCIÓN RETROACTIVA:

1. Accede al Dashboard del sistema: http://localhost:5000/dashboard

2. El sistema DEBERÍA:
   ✓ Detectar que faltan asistencias de esos {len(dias_a_borrar)} días
   ✓ Crear automáticamente ausencias con estado PENDIENTE
   ✓ Mostrar el BANNER ROJO con las alertas de ausencias

3. Verifica en consola del servidor Flask:
   Deberías ver: "✅ Creadas X ausencias retroactivas de días faltantes"

4. En el Dashboard verás:
   🚨 Banner rojo con empleados que tienen ausencias pendientes
   📋 Listado de todos los empleados con días sin justificar

NOTA: Si no ves el banner, verifica:
- Que el servidor Flask esté corriendo
- Que haya empleados ACTIVOS en el sistema
- Revisa la consola del servidor para mensajes de debug
        """)
        
        return True

if __name__ == '__main__':
    try:
        resultado = generar_datos_prueba()
        if not resultado:
            exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
