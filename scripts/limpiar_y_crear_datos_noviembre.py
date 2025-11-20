"""
Script todo-en-uno para limpiar datos históricos y generar datos de prueba de Noviembre 2025

CARACTERÍSTICAS:
✓ Limpia todas las tablas de datos históricos (asistencias, permisos, sanciones, vacaciones, liquidaciones, etc.)
✓ Mantiene intactos: Usuarios, Empleados, Cargos, Contratos, Empresas
✓ Genera datos realistas de Noviembre 2025:
  - Asistencias variadas (presentes, tardanzas, ausencias)
  - Vacaciones de 2-3 días para algunos empleados
  - Permisos ocasionales (médicos, personales)
  - Llegadas tardías realistas
  - Algunos descuentos y sanciones

MODO DE USO:
    # Ver qué se va a eliminar (modo seguro)
    python scripts\limpiar_y_crear_datos_noviembre.py --dry-run

    # Ejecutar limpieza y generación de datos
    python scripts\limpiar_y_crear_datos_noviembre.py --ejecutar

IMPORTANTE: Haz backup de tu BD antes de ejecutar con --ejecutar
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal
import calendar
import random
import argparse

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import (
    Empleado, Asistencia, Descuento, Sancion, Vacacion, Permiso,
    Liquidacion, IngresoExtra, EstadoEmpleadoEnum, Anticipo,
    BonificacionFamiliar, Despido
)
from sqlalchemy import func

# ============================================
# CONFIGURACIÓN
# ============================================
AÑO = 2025
MES = 11  # Noviembre

TABLAS_A_LIMPIAR = [
    (Asistencia, 'asistencias'),
    (Permiso, 'permisos'),
    (Sancion, 'sanciones'),
    (Vacacion, 'vacaciones'),
    (Liquidacion, 'liquidaciones'),
    (IngresoExtra, 'ingresos_extras'),
    (Descuento, 'descuentos'),
    (Anticipo, 'anticipos'),
    (BonificacionFamiliar, 'bonificaciones_familiares'),
    (Despido, 'despidos'),
]

# ============================================
# FUNCIONES DE LIMPIEZA
# ============================================

def mostrar_conteos(app):
    """Muestra los conteos actuales de cada tabla"""
    print('\n' + '='*60)
    print('📊 CONTEO ACTUAL DE DATOS')
    print('='*60)
    
    with app.app_context():
        for modelo, nombre in TABLAS_A_LIMPIAR:
            try:
                cnt = db.session.query(func.count(modelo.id)).scalar()
                print(f'  {nombre:30s}: {cnt:5d} registros')
            except Exception as e:
                print(f'  {nombre:30s}: ERROR - {str(e)[:50]}')


def limpiar_datos(app, dry_run=True):
    """Limpia todas las tablas de datos históricos"""
    
    if dry_run:
        print('\n' + '='*60)
        print('🔍 MODO DRY-RUN: Solo mostrando lo que se eliminaría')
        print('='*60)
        mostrar_conteos(app)
        print('\n⚠️  Para ejecutar realmente la limpieza, usa: --ejecutar')
        return
    
    print('\n' + '='*60)
    print('🗑️  LIMPIANDO DATOS HISTÓRICOS')
    print('='*60)
    
    with app.app_context():
        total_eliminados = 0
        for modelo, nombre in TABLAS_A_LIMPIAR:
            try:
                eliminados = db.session.query(modelo).delete()
                db.session.commit()
                print(f'  ✓ {nombre:30s}: {eliminados:5d} registros eliminados')
                total_eliminados += eliminados
            except Exception as e:
                db.session.rollback()
                print(f'  ✗ {nombre:30s}: ERROR - {e}')
        
        print(f'\n  Total eliminados: {total_eliminados} registros')
        print('  ✓ Limpieza completada')


# ============================================
# FUNCIONES DE GENERACIÓN DE DATOS
# ============================================

def obtener_dias_habiles(año, mes):
    """Obtiene todos los días hábiles (lunes a viernes) del mes"""
    primer_dia = date(año, mes, 1)
    ultimo_dia = date(año, mes, calendar.monthrange(año, mes)[1])
    
    dias_habiles = []
    fecha_actual = primer_dia
    while fecha_actual <= ultimo_dia:
        if fecha_actual.weekday() < 5:  # Lunes a viernes
            dias_habiles.append(fecha_actual)
        fecha_actual += timedelta(days=1)
    
    return dias_habiles


def generar_asistencias_realistas(app, empleados, dias_habiles):
    """Genera asistencias realistas con variedad de situaciones"""
    
    print('\n' + '='*60)
    print('📝 GENERANDO ASISTENCIAS DE NOVIEMBRE 2025')
    print('='*60)
    print(f'  Empleados: {len(empleados)}')
    print(f'  Días hábiles: {len(dias_habiles)} ({dias_habiles[0]} a {dias_habiles[-1]})')
    
    with app.app_context():
        from sqlalchemy import text
        
        contador = {
            'presentes': 0,
            'tardanzas': 0,
            'ausencias': 0,
            'vacaciones': 0,
            'permisos': 0
        }
        
        # Asignar vacaciones a 2-3 empleados aleatorios
        empleados_con_vacaciones = random.sample(empleados, min(3, len(empleados)))
        vacaciones_asignadas = {}
        
        for emp in empleados_con_vacaciones:
            # Vacaciones de 2-3 días consecutivos
            duracion = random.randint(2, 3)
            inicio_idx = random.randint(0, len(dias_habiles) - duracion)
            dias_vacacionales = dias_habiles[inicio_idx:inicio_idx + duracion]
            vacaciones_asignadas[emp.id] = dias_vacacionales
            
            # Crear registro de vacación (solicitud aprobada)
            from app.models import EstadoVacacionEnum
            vacacion = Vacacion(
                empleado_id=emp.id,
                año=AÑO,
                dias_disponibles=15,
                dias_tomados=duracion,
                dias_pendientes=15 - duracion,
                fecha_inicio_solicitud=dias_vacacionales[0],
                fecha_fin_solicitud=dias_vacacionales[-1],
                estado=EstadoVacacionEnum.APROBADA
            )
            db.session.add(vacacion)
            contador['vacaciones'] += 1
        
        # Asignar algunos permisos a empleados aleatorios
        empleados_con_permisos = random.sample(empleados, min(2, len(empleados)))
        permisos_asignados = {}
        
        for emp in empleados_con_permisos:
            # 1-2 permisos en el mes
            num_permisos = random.randint(1, 2)
            dias_permiso = random.sample(dias_habiles, num_permisos)
            permisos_asignados[emp.id] = dias_permiso
            
            for dia_permiso in dias_permiso:
                from app.models import EstadoPermisoEnum
                tipo_permiso = random.choice(['Enfermedad', 'Asunto Personal', 'Trámite Médico'])
                con_goce = random.choice([True, False])
                
                permiso = Permiso(
                    empleado_id=emp.id,
                    tipo_permiso=tipo_permiso,
                    motivo=f"Solicitud de permiso por {tipo_permiso.lower()}",
                    fecha_inicio=dia_permiso,
                    fecha_fin=dia_permiso,
                    dias_solicitados=1,
                    estado=EstadoPermisoEnum.APROBADO,
                    con_goce=con_goce,
                    observaciones=f"Permiso {tipo_permiso.lower()} - 1 día"
                )
                db.session.add(permiso)
                contador['permisos'] += 1
        
        # Contadores adicionales
        contador['solo_manana'] = 0
        contador['solo_tarde'] = 0
        contador['salida_anticipada'] = 0
        contador['almuerzo_largo'] = 0
        contador['sin_almuerzo'] = 0
        
        # Generar asistencias VARIADAS para cada empleado (Nivel 2: Observaciones Detalladas)
        for empleado in empleados:
            for dia in dias_habiles:
                # Verificar si está de vacaciones
                if empleado.id in vacaciones_asignadas:
                    if dia in vacaciones_asignadas[empleado.id]:
                        sql = text("""
                            INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                            VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                        """)
                        db.session.execute(sql, {
                            'emp_id': empleado.id,
                            'fecha': dia,
                            'hora_ent': datetime.strptime("08:00", "%H:%M").time(),
                            'hora_sal': datetime.strptime("17:00", "%H:%M").time(),
                            'presente': True,
                            'obs': 'Vacaciones pagadas'
                        })
                        contador['presentes'] += 1
                        continue
                
                # Verificar si tiene permiso con goce
                if empleado.id in permisos_asignados:
                    if dia in permisos_asignados[empleado.id]:
                        sql = text("""
                            INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                            VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                        """)
                        db.session.execute(sql, {
                            'emp_id': empleado.id,
                            'fecha': dia,
                            'hora_ent': datetime.strptime("08:00", "%H:%M").time(),
                            'hora_sal': datetime.strptime("17:00", "%H:%M").time(),
                            'presente': True,
                            'obs': 'Permiso con goce de sueldo'
                        })
                        contador['presentes'] += 1
                        continue
                
                # Generar diferentes tipos de asistencias con probabilidades
                rand = random.random()
                
                # 5% Ausencia completa
                if rand < 0.05:
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'presente': False,
                        'obs': 'Ausencia injustificada - Sin marcaciones'
                    })
                    contador['ausencias'] += 1
                
                # 3% Solo vino a la mañana (no regresó)
                elif rand < 0.08:
                    hora_ent = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=random.randint(0, 20))
                    hora_sal = datetime.strptime("12:00", "%H:%M") + timedelta(minutes=random.randint(-10, 10))
                    tardanza = (hora_ent - datetime.strptime("08:00", "%H:%M")).seconds // 60
                    
                    if tardanza > 0:
                        obs = f"Llegada tarde {tardanza} min - Solo turno mañana - No regresó"
                    else:
                        obs = "Solo turno mañana - No regresó del almuerzo"
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': obs
                    })
                    contador['solo_manana'] += 1
                
                # 2% Solo vino a la tarde
                elif rand < 0.10:
                    hora_ent = datetime.strptime("13:00", "%H:%M") + timedelta(minutes=random.randint(0, 30))
                    hora_sal = datetime.strptime("17:00", "%H:%M")
                    horas = ((hora_sal - hora_ent).seconds // 3600)
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': f'Solo turno tarde ({horas}h)'
                    })
                    contador['solo_tarde'] += 1
                
                # 3% Salida anticipada
                elif rand < 0.13:
                    minutos_tarde = random.randint(0, 30)
                    hora_ent = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=minutos_tarde)
                    hora_sal = datetime.strptime("15:00", "%H:%M") + timedelta(minutes=random.randint(-30, 0))
                    
                    if minutos_tarde > 0:
                        obs = f"Llegada tarde {minutos_tarde} min - Salida anticipada {hora_sal.strftime('%H:%M')}"
                    else:
                        obs = f"Salida anticipada {hora_sal.strftime('%H:%M')}"
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': obs
                    })
                    contador['salida_anticipada'] += 1
                
                # 15% Llegada tarde con día completo y almuerzo
                elif rand < 0.28:
                    minutos_tarde = random.randint(10, 90)
                    hora_ent = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=minutos_tarde)
                    hora_sal = datetime.strptime("17:00", "%H:%M")
                    duracion_almuerzo = random.randint(30, 90)
                    
                    if minutos_tarde >= 60:
                        horas = minutos_tarde // 60
                        mins = minutos_tarde % 60
                        if mins > 0:
                            tardanza_str = f"{horas}h {mins}min"
                        else:
                            tardanza_str = f"{horas}h"
                    else:
                        tardanza_str = f"{minutos_tarde} min"
                    
                    if duracion_almuerzo <= 60:
                        almuerzo_str = f"{duracion_almuerzo}min"
                    else:
                        h = duracion_almuerzo // 60
                        m = duracion_almuerzo % 60
                        almuerzo_str = f"{h}h {m}min" if m > 0 else f"{h}h"
                    
                    obs = f"Llegada tarde {tardanza_str} - Día completo - Almuerzo {almuerzo_str}"
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': obs
                    })
                    contador['tardanzas'] += 1
                
                # 10% Día completo con almuerzo largo (>1h)
                elif rand < 0.38:
                    hora_ent = datetime.strptime("08:00", "%H:%M")
                    hora_sal = datetime.strptime("17:00", "%H:%M")
                    duracion_almuerzo = random.randint(75, 150)
                    
                    h = duracion_almuerzo // 60
                    m = duracion_almuerzo % 60
                    almuerzo_str = f"{h}h {m}min" if m > 0 else f"{h}h"
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': f'Día completo (8h) - Almuerzo {almuerzo_str}'
                    })
                    contador['almuerzo_largo'] += 1
                
                # 20% Día completo normal con almuerzo 1h
                elif rand < 0.58:
                    hora_ent = datetime.strptime("08:00", "%H:%M")
                    hora_sal = datetime.strptime("17:00", "%H:%M")
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': 'Día completo (8h) - Almuerzo 1h'
                    })
                    contador['presentes'] += 1
                
                # 42% Día completo sin registro de almuerzo
                else:
                    hora_ent = datetime.strptime("08:00", "%H:%M")
                    hora_sal = datetime.strptime("17:00", "%H:%M")
                    
                    sql = text("""
                        INSERT INTO asistencias (empleado_id, fecha, hora_entrada, hora_salida, presente, observaciones, fecha_creacion)
                        VALUES (:emp_id, :fecha, :hora_ent, :hora_sal, :presente, :obs, NOW())
                    """)
                    db.session.execute(sql, {
                        'emp_id': empleado.id,
                        'fecha': dia,
                        'hora_ent': hora_ent.time(),
                        'hora_sal': hora_sal.time(),
                        'presente': True,
                        'obs': 'Día completo - Sin registro de almuerzo'
                    })
                    contador['sin_almuerzo'] += 1
        
        db.session.commit()
        
        print(f'\n  ✓ Asistencias creadas (Nivel 2 - Observaciones Detalladas):')
        print(f'    - Días completos normales: {contador["presentes"]}')
        print(f'    - Días completos sin almuerzo: {contador["sin_almuerzo"]}')
        print(f'    - Días completos con almuerzo largo: {contador["almuerzo_largo"]}')
        print(f'    - Llegadas tardías: {contador["tardanzas"]}')
        print(f'    - Solo turno mañana: {contador["solo_manana"]}')
        print(f'    - Solo turno tarde: {contador["solo_tarde"]}')
        print(f'    - Salidas anticipadas: {contador["salida_anticipada"]}')
        print(f'    - Ausencias: {contador["ausencias"]}')
        print(f'  ✓ Vacaciones: {contador["vacaciones"]} períodos')
        print(f'  ✓ Permisos: {contador["permisos"]} días')


def generar_descuentos_y_sanciones(app, empleados):
    """Genera algunos descuentos y sanciones de ejemplo"""
    
    print('\n' + '='*60)
    print('💰 GENERANDO DESCUENTOS Y SANCIONES')
    print('='*60)
    
    with app.app_context():
        # Algunos descuentos manuales
        empleados_con_descuentos = random.sample(empleados, min(2, len(empleados)))
        
        for emp in empleados_con_descuentos:
            monto = Decimal(random.choice([50000, 100000, 150000]))
            descuento = Descuento(
                empleado_id=emp.id,
                tipo='Adelanto de Sueldo',
                monto=monto,
                descripcion='Descuento por adelanto de sueldo solicitado',
                mes=MES,
                año=AÑO,
                activo=True,
                origen_tipo='manual'
            )
            db.session.add(descuento)
        
        print(f'  ✓ {len(empleados_con_descuentos)} descuentos manuales creados')
        
        # Algunas sanciones
        empleados_con_sanciones = random.sample(
            [e for e in empleados if e not in empleados_con_descuentos], 
            min(2, len(empleados) - len(empleados_con_descuentos))
        )
        
        for emp in empleados_con_sanciones:
            tipo_sancion = random.choice(['Amonestación Escrita', 'Descuento por Falta', 'Suspensión'])
            monto = Decimal(random.choice([0, 50000, 100000])) if tipo_sancion != 'Amonestación Escrita' else Decimal(0)
            
            sancion = Sancion(
                empleado_id=emp.id,
                tipo_sancion=tipo_sancion,
                motivo=f'{tipo_sancion} por llegadas tardías reiteradas',
                monto=monto,
                fecha=date(AÑO, MES, random.randint(10, 15)),
                descripcion=f'Sanción aplicada el {date(AÑO, MES, random.randint(10, 15))}'
            )
            db.session.add(sancion)
        
        db.session.commit()
        print(f'  ✓ {len(empleados_con_sanciones)} sanciones creadas')


def generar_datos_noviembre(app):
    """Genera todos los datos de prueba de noviembre"""
    
    print('\n' + '='*60)
    print('✨ GENERANDO DATOS DE NOVIEMBRE 2025')
    print('='*60)
    
    with app.app_context():
        # Obtener empleados activos
        empleados = Empleado.query.filter_by(estado=EstadoEmpleadoEnum.ACTIVO).all()
        
        if len(empleados) == 0:
            print('\n❌ ERROR: No hay empleados activos en la base de datos')
            return False
        
        print(f'\n✓ Empleados activos encontrados: {len(empleados)}')
        for emp in empleados:
            print(f'  - {emp.nombre_completo} (ID: {emp.id})')
        
        # Obtener días hábiles de noviembre
        dias_habiles = obtener_dias_habiles(AÑO, MES)
        
        # Generar datos
        generar_asistencias_realistas(app, empleados, dias_habiles)
        generar_descuentos_y_sanciones(app, empleados)
        
        return True


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description='Limpia datos históricos y genera datos de prueba de Noviembre 2025'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Muestra qué se eliminaría sin hacer cambios (modo seguro)'
    )
    parser.add_argument(
        '--ejecutar',
        action='store_true',
        help='Ejecuta la limpieza y generación de datos (DESTRUCTIVO)'
    )
    
    args = parser.parse_args()
    
    # Si no se especifica nada, usar dry-run por defecto
    if not args.dry_run and not args.ejecutar:
        args.dry_run = True
    
    # Crear app
    app = create_app('development')
    
    print('\n' + '='*60)
    print('🚀 SCRIPT DE LIMPIEZA Y GENERACIÓN DE DATOS')
    print('='*60)
    print(f'  Período: Noviembre {AÑO}')
    print(f'  Fecha actual: {date.today()}')
    
    if args.dry_run:
        print('\n⚠️  MODO SEGURO (DRY-RUN): No se harán cambios')
        print('  Para ejecutar realmente, usa: --ejecutar')
        mostrar_conteos(app)
        print('\n' + '='*60)
        print('📋 RESUMEN DE LO QUE SE HARÍA')
        print('='*60)
        print('  1. Eliminar todos los datos de las tablas de históricos')
        print('  2. Mantener intactos: Usuarios, Empleados, Cargos, Contratos')
        print('  3. Generar datos de Noviembre 2025:')
        print('     - Asistencias variadas (presentes, tardanzas, ausencias)')
        print('     - Vacaciones para 2-3 empleados (2-3 días)')
        print('     - Permisos ocasionales')
        print('     - Algunos descuentos y sanciones')
        print('\n⚠️  IMPORTANTE: Haz backup antes de ejecutar con --ejecutar')
        return
    
    if args.ejecutar:
        print('\n⚠️  MODO EJECUCIÓN: Se harán cambios REALES en la base de datos')
        print('\n¿Estás seguro? Escribe "SI" para continuar: ', end='')
        confirmacion = input().strip().upper()
        
        if confirmacion != 'SI':
            print('\n❌ Operación cancelada')
            return
        
        # Ejecutar limpieza
        limpiar_datos(app, dry_run=False)
        
        # Generar datos nuevos
        resultado = generar_datos_noviembre(app)
        
        if resultado:
            print('\n' + '='*60)
            print('✅ PROCESO COMPLETADO EXITOSAMENTE')
            print('='*60)
            print('\n📋 PRÓXIMOS PASOS:')
            print('  1. Ve a: Menú → Asistencia → Ver registros')
            print('  2. Revisa las asistencias de Noviembre 2025')
            print('  3. Genera liquidaciones: Menú → Nómina → Generar')
            print('  4. Selecciona período: 2025-11 (noviembre)')
            print('\n💡 TIP: Los datos incluyen:')
            print('  • Llegadas tardías (marcadas en observaciones)')
            print('  • Ausencias injustificadas')
            print('  • Vacaciones de 2-3 días')
            print('  • Permisos aprobados')
            print('  • Descuentos y sanciones de ejemplo')
        else:
            print('\n❌ Hubo errores durante la generación de datos')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n❌ Operación cancelada por el usuario')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ ERROR FATAL: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
