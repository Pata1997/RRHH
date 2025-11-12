"""
Script para generar datos de prueba realistas.

Crea:
- Asistencias completas de octubre para los 6 empleados
- Descuentos manuales para 3 empleados
- Sanciones con descuentos automáticos para otros 3 empleados

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
    """Genera datos realistas de prueba"""
    
    with app.app_context():
        print("=" * 60)
        print("GENERADOR DE DATOS DE PRUEBA")
        print("=" * 60)
        
        # Obtener los empleados activos
        empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
        
        if len(empleados) < 5:
            print(f"\n❌ ERROR: Solo hay {len(empleados)} empleados. Se necesitan al menos 5.")
            return False
        
        print(f"\n✓ Encontrados {len(empleados)} empleados:")
        for emp in empleados:
            print(f"  - {emp.nombre_completo} (ID: {emp.id})")
        
        # Octubre 2025
        año = 2025
        mes = 10
        
        # Obtener días hábiles de octubre (lunes a viernes)
        primer_día = date(año, mes, 1)
        último_día = date(año, mes, calendar.monthrange(año, mes)[1])
        
        días_hábiles = []
        fecha_actual = primer_día
        while fecha_actual <= último_día:
            # Lunes = 0, Domingo = 6
            if fecha_actual.weekday() < 5:  # Lunes a viernes
                días_hábiles.append(fecha_actual)
            fecha_actual += timedelta(days=1)
        
        print(f"\n📅 Octubre {año}: {len(días_hábiles)} días hábiles")
        print(f"   Rango: {primer_día.strftime('%d/%m')} - {último_día.strftime('%d/%m')}")
        
        # ============================================
        # 1. GENERAR ASISTENCIAS (TODOS PRESENTE)
        # ============================================
        print(f"\n📝 Generando asistencias...")
        
        contador_asistencias = 0
        for empleado in empleados:
            for día in días_hábiles:
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
                        observaciones="Presente"
                    )
                    db.session.add(asistencia)
                    contador_asistencias += 1
        
        db.session.commit()
        print(f"   ✓ {contador_asistencias} asistencias creadas ({len(empleados)} × {len(días_hábiles)} días)")
        
        # ============================================
        # 2. AGREGAR DESCUENTOS A 3 EMPLEADOS (SALTADO)
        # ============================================
        print(f"\n💰 Descuentos: Requieren migración de BD (columna 'activo')")
        print(f"   [Saltado por ahora - La BD necesita: ALTER TABLE descuentos ADD COLUMN activo BOOLEAN DEFAULT TRUE]")
        
        # ============================================
        # 3. AGREGAR SANCIONES (SALTADO)
        # ============================================
        print(f"\n⚠️  Sanciones: Saltadas por ahora (dependen de descuentos)")
        
        # ============================================
        # RESUMEN FINAL
        # ============================================
        print(f"\n" + "=" * 60)
        print("✅ DATOS DE PRUEBA GENERADOS")
        print("=" * 60)
        
        print(f"""
RESUMEN:
✓ Asistencias: {len(empleados)} empleados × {len(días_hábiles)} días = {contador_asistencias} registros
⚠️  Descuentos: Requieren migración (se pueden agregar después)
⚠️  Sanciones: Requieren migración (se pueden agregar después)

PRÓXIMO PASO:
1. Ejecuta la migración de BD:
   ALTER TABLE descuentos ADD COLUMN activo BOOLEAN DEFAULT TRUE;

DESPUÉS PODRÁS:
1. Ir a: Menú → Nómina → Generar (liquidaciones)
2. Seleccionar período: 2025-10 (octubre)
3. Ver las liquidaciones con:
   - Salario base
   - Ingresos extras (si hay)
   - Aporte IPS
   - Salario neto


PRÓXIMAS PRUEBAS:
- Registrar un despido y ver liquidación automática
- Generar aguinaldos de 2025
- Descargar PDFs
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
