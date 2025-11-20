"""
Script para resetear BD y generar datos de prueba de Noviembre 2025

IMPORTANTE: Este script:
1. ELIMINA todos los datos EXCEPTO: usuarios, empleados, cargos, empresa
2. GENERA datos realistas de noviembre (1-19)
3. NO genera liquidación (para que lo hagas en vivo)

Uso: python scripts/reset_y_datos_noviembre.py
"""

import os
import sys
from datetime import date, datetime, time, timedelta
from random import randint, choice, random
from decimal import Decimal

# Agregar el directorio raíz al path para importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import (
    Empleado, Asistencia, AsistenciaEvento, Permiso, Vacacion, 
    Sancion, Anticipo, IngresoExtra, HorasExtra, Descuento, 
    Liquidacion, BonificacionFamiliar, Despido, Postulante, 
    DocumentosCurriculum, Bitacora, Contrato,
    EstadoPermisoEnum, EstadoVacacionEnum, TipoHijoEnum
)

# ===================== CONFIGURACIÓN =====================
DIAS_SIMULAR = 19  # 1-19 noviembre (hasta hoy)
MES = 11
AÑO = 2025

# Porcentajes y probabilidades
PROB_AUSENCIA = 0.05  # 5% de ausencias
PROB_TARDE = 0.10     # 10% llegadas tarde
PROB_SALIDA_TEMPRANO = 0.05  # 5% salidas antes de hora

# Cantidad de eventos especiales
EMPLEADOS_CON_VACACIONES = 2
EMPLEADOS_CON_ANTICIPOS = 2
EMPLEADOS_CON_BONIFICACION = 2
EMPLEADOS_CON_HORAS_EXTRA = 2

GENERAR_LIQUIDACION = False  # Cambiar a True si quieres que genere liquidación

# ===================== FUNCIONES =====================

def limpiar_base_datos():
    """Limpia todas las tablas EXCEPTO usuarios, empleados, cargos, empresa"""
    print("\n" + "="*80)
    print("🧹 PASO 1: LIMPIANDO BASE DE DATOS")
    print("="*80)
    
    try:
        # Orden importante: eliminar primero las tablas con foreign keys
        
        print("Eliminando bitácora...")
        count = db.session.query(Bitacora).delete()
        print(f"   ✅ {count} registros eliminados")
        
        print("Eliminando documentos curriculum...")
        count = db.session.query(DocumentosCurriculum).delete()
        print(f"   ✅ {count} documentos eliminados")
        
        print("Eliminando postulantes...")
        count = db.session.query(Postulante).delete()
        print(f"   ✅ {count} postulantes eliminados")
        
        print("Eliminando despidos...")
        count = db.session.query(Despido).delete()
        print(f"   ✅ {count} despidos eliminados")
        
        print("Eliminando liquidaciones...")
        count = db.session.query(Liquidacion).delete()
        print(f"   ✅ {count} liquidaciones eliminadas")
        
        print("Eliminando contratos...")
        count = db.session.query(Contrato).delete()
        print(f"   ✅ {count} contratos eliminados")
        
        print("Eliminando bonificaciones familiares...")
        count = db.session.query(BonificacionFamiliar).delete()
        print(f"   ✅ {count} bonificaciones eliminadas")
        
        print("Eliminando descuentos...")
        count = db.session.query(Descuento).delete()
        print(f"   ✅ {count} descuentos eliminados")
        
        print("Eliminando horas extra...")
        count = db.session.query(HorasExtra).delete()
        print(f"   ✅ {count} horas extra eliminadas")
        
        print("Eliminando ingresos extra...")
        count = db.session.query(IngresoExtra).delete()
        print(f"   ✅ {count} ingresos extra eliminados")
        
        print("Eliminando anticipos...")
        count = db.session.query(Anticipo).delete()
        print(f"   ✅ {count} anticipos eliminados")
        
        print("Eliminando sanciones...")
        count = db.session.query(Sancion).delete()
        print(f"   ✅ {count} sanciones eliminadas")
        
        print("Eliminando vacaciones...")
        count = db.session.query(Vacacion).delete()
        print(f"   ✅ {count} vacaciones eliminadas")
        
        print("Eliminando permisos...")
        count = db.session.query(Permiso).delete()
        print(f"   ✅ {count} permisos eliminados")
        
        print("Eliminando eventos de asistencia...")
        count = db.session.query(AsistenciaEvento).delete()
        print(f"   ✅ {count} eventos eliminados")
        
        print("Eliminando asistencias...")
        count = db.session.query(Asistencia).delete()
        print(f"   ✅ {count} asistencias eliminadas")
        
        db.session.commit()
        
        # Contar lo que quedó
        usuarios_count = db.session.query(db.func.count(db.text('id'))).select_from(db.text('usuarios')).scalar()
        empleados_count = db.session.query(Empleado).count()
        
        print("\n📊 MANTENIDOS:")
        print(f"   - {usuarios_count} usuarios")
        print(f"   - {empleados_count} empleados")
        
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERROR al limpiar: {e}")
        return False


def generar_asistencias_noviembre(empleados):
    """Genera asistencias realistas para noviembre 1-19"""
    print("\n📅 Generando asistencias (1-19 noviembre)...")
    
    for empleado in empleados:
        presentes = 0
        ausentes = 0
        tardes = 0
        
        for dia in range(1, DIAS_SIMULAR + 1):
            fecha = date(AÑO, MES, dia)
            
            # Saltar fines de semana
            if fecha.weekday() >= 5:  # 5=sábado, 6=domingo
                continue
            
            # Verificar si está de vacaciones
            tiene_vacaciones = db.session.query(Vacacion).filter(
                Vacacion.empleado_id == empleado.id,
                Vacacion.fecha_inicio <= fecha,
                Vacacion.fecha_fin >= fecha,
                Vacacion.estado == EstadoVacacionEnum.APROBADA
            ).first()
            
            if tiene_vacaciones:
                continue
            
            # Determinar si hay ausencia aleatoria
            if random() < PROB_AUSENCIA:
                # Ausencia
                asistencia = Asistencia(
                    empleado_id=empleado.id,
                    fecha=fecha,
                    presente=False,
                    hora_entrada=None,
                    hora_salida=None,
                    justificacion_estado='INJUSTIFICADO'
                )
                db.session.add(asistencia)
                ausentes += 1
                continue
            
            # Generar entrada
            entrada_base = time(8, 0)  # 08:00
            
            # Determinar si llega tarde
            if random() < PROB_TARDE:
                # Tarde entre 8:05 y 8:30
                minutos_tarde = randint(5, 30)
                hora_entrada = time(8, minutos_tarde)
                tardes += 1
            else:
                # A tiempo o temprano (7:50 - 8:00)
                minutos = randint(-10, 0)
                if minutos < 0:
                    hora_entrada = time(7, 60 + minutos)
                else:
                    hora_entrada = time(8, 0)
            
            # Generar salida
            if random() < PROB_SALIDA_TEMPRANO:
                # Sale temprano (16:30 - 16:55)
                hora_salida = time(16, randint(30, 55))
            else:
                # Sale normal o tarde (17:00 - 17:30)
                hora_salida = time(17, randint(0, 30))
            
            # Crear asistencia
            asistencia = Asistencia(
                empleado_id=empleado.id,
                fecha=fecha,
                presente=True,
                hora_entrada=hora_entrada,
                hora_salida=hora_salida,
                justificacion_estado='N/A'
            )
            db.session.add(asistencia)
            db.session.flush()
            
            # Crear eventos de entrada/salida
            evento_entrada = AsistenciaEvento(
                empleado_id=empleado.id,
                tipo='ENTRADA',
                timestamp=datetime.combine(fecha, hora_entrada)
            )
            evento_salida = AsistenciaEvento(
                empleado_id=empleado.id,
                tipo='SALIDA',
                timestamp=datetime.combine(fecha, hora_salida)
            )
            db.session.add(evento_entrada)
            db.session.add(evento_salida)
            
            presentes += 1
        
        print(f"   ✅ {empleado.codigo} {empleado.nombre}: {presentes} presentes, {ausentes} ausentes, {tardes} tardes")
    
    db.session.commit()


def generar_vacaciones(empleados):
    """Genera vacaciones para algunos empleados"""
    print("\n🏖️  Generando vacaciones...")
    
    empleados_seleccionados = empleados[:EMPLEADOS_CON_VACACIONES]
    
    periodos_vacaciones = [
        (date(2025, 11, 11), date(2025, 11, 13)),  # 3 días
        (date(2025, 11, 18), date(2025, 11, 19)),  # 2 días
    ]
    
    for i, empleado in enumerate(empleados_seleccionados):
        if i < len(periodos_vacaciones):
            inicio, fin = periodos_vacaciones[i]
            dias = (fin - inicio).days + 1
            
            vacacion = Vacacion(
                empleado_id=empleado.id,
                fecha_solicitud=date(2025, 10, 25),  # Solicitó en octubre
                fecha_inicio=inicio,
                fecha_fin=fin,
                dias_solicitados=dias,
                motivo='Vacaciones programadas',
                estado=EstadoVacacionEnum.APROBADA,
                fecha_revision=date(2025, 10, 26),
                aprobado_rechazado_por='admin'
            )
            db.session.add(vacacion)
            print(f"   ✅ {empleado.nombre}: {inicio} a {fin} ({dias} días) - APROBADAS")
    
    db.session.commit()


def generar_sanciones(empleados):
    """Genera sanciones por llegadas tarde"""
    print("\n⚠️  Generando sanciones...")
    
    # Buscar empleados que llegaron tarde más de 2 veces
    for empleado in empleados:
        llegadas_tarde = db.session.query(Asistencia).filter(
            Asistencia.empleado_id == empleado.id,
            Asistencia.presente == True,
            Asistencia.hora_entrada > time(8, 5)
        ).count()
        
        if llegadas_tarde >= 2:
            # Crear sanción por llegadas tarde
            monto = Decimal('50000') * llegadas_tarde
            sancion = Sancion(
                empleado_id=empleado.id,
                tipo_sancion='Descuento',
                fecha=date(2025, 11, 15),
                monto=monto,
                descripcion=f'Descuento por {llegadas_tarde} llegadas tarde en noviembre'
            )
            db.session.add(sancion)
            db.session.flush()
            
            # Crear descuento automático
            descuento = Descuento(
                empleado_id=empleado.id,
                concepto=f'Sanción: {llegadas_tarde} llegadas tarde',
                monto=monto,
                mes=11,
                año=2025
            )
            db.session.add(descuento)
            
            print(f"   ✅ {empleado.nombre}: {llegadas_tarde} llegadas tarde - ₲{monto:,.0f}")
    
    db.session.commit()


def generar_anticipos(empleados):
    """Genera anticipos del mes"""
    print("\n💰 Generando anticipos...")
    
    empleados_seleccionados = empleados[:EMPLEADOS_CON_ANTICIPOS]
    
    fechas = [date(2025, 11, 5), date(2025, 11, 8)]
    montos = [300000, 200000]
    
    for i, empleado in enumerate(empleados_seleccionados):
        if i < len(fechas):
            anticipo = Anticipo(
                empleado_id=empleado.id,
                monto=Decimal(str(montos[i])),
                fecha_solicitud=fechas[i] - timedelta(days=1),
                fecha_aprobacion=fechas[i],
                motivo='Gastos personales',
                aprobado=True,
                aplicado=False,
                aprobado_por='admin'
            )
            db.session.add(anticipo)
            print(f"   ✅ {empleado.nombre}: ₲{montos[i]:,} ({fechas[i]}) - APROBADO, NO APLICADO")
    
    db.session.commit()


def generar_ingresos_extras(empleados):
    """Genera bonos y horas extra"""
    print("\n💵 Generando ingresos extras...")
    
    # Bonos
    if len(empleados) > 0:
        bono = IngresoExtra(
            empleado_id=empleados[0].id,
            concepto='Bono productividad',
            monto=Decimal('150000'),
            mes=11,
            año=2025,
            estado='APROBADO',
            aplicado=False
        )
        db.session.add(bono)
        print(f"   ✅ {empleados[0].nombre}: Bono productividad ₲150,000")
    
    # Horas extra
    empleados_horas = empleados[:EMPLEADOS_CON_HORAS_EXTRA]
    for i, empleado in enumerate(empleados_horas):
        horas = randint(3, 8)
        tasa = Decimal('20000')
        
        for _ in range(horas):
            hora_extra = HorasExtra(
                empleado_id=empleado.id,
                fecha=date(2025, 11, randint(10, 18)),
                cantidad_horas=Decimal('1'),
                tasa_por_hora=tasa,
                motivo='Trabajo extra',
                estado='APROBADO',
                aplicado=False
            )
            db.session.add(hora_extra)
        
        total = tasa * horas
        print(f"   ✅ {empleado.nombre}: {horas} horas extra (₲{total:,.0f})")
    
    db.session.commit()


def generar_permisos(empleados):
    """Genera permisos médicos y personales"""
    print("\n📋 Generando permisos...")
    
    if len(empleados) >= 2:
        # Permiso médico aprobado
        permiso1 = Permiso(
            empleado_id=empleados[0].id,
            tipo_permiso='Médico',
            fecha_solicitud=date(2025, 11, 6),
            fecha_inicio=date(2025, 11, 7),
            fecha_fin=date(2025, 11, 7),
            dias=1,
            motivo='Consulta médica',
            estado=EstadoPermisoEnum.APROBADO,
            fecha_revision=date(2025, 11, 6),
            aprobado_rechazado_por='admin'
        )
        db.session.add(permiso1)
        print(f"   ✅ {empleados[0].nombre}: Médico (7 nov) - APROBADO")
        
        # Permiso personal rechazado
        permiso2 = Permiso(
            empleado_id=empleados[1].id,
            tipo_permiso='Personal',
            fecha_solicitud=date(2025, 11, 11),
            fecha_inicio=date(2025, 11, 12),
            fecha_fin=date(2025, 11, 12),
            dias=1,
            motivo='Trámite personal',
            estado=EstadoPermisoEnum.RECHAZADO,
            fecha_revision=date(2025, 11, 11),
            aprobado_rechazado_por='admin',
            comentario_revision='No hay cobertura suficiente'
        )
        db.session.add(permiso2)
        print(f"   ✅ {empleados[1].nombre}: Personal (12 nov) - RECHAZADO")
    
    db.session.commit()


def generar_bonificaciones_familiares(empleados):
    """Genera bonificaciones familiares (hijos)"""
    print("\n👨‍👩‍👧 Generando bonificaciones familiares...")
    
    empleados_seleccionados = empleados[:EMPLEADOS_CON_BONIFICACION]
    
    hijos_data = [
        {'cantidad': 2, 'nombres': ['Juan Jr.', 'María']},
        {'cantidad': 1, 'nombres': ['Pedro']},
    ]
    
    for i, empleado in enumerate(empleados_seleccionados):
        if i < len(hijos_data):
            for nombre in hijos_data[i]['nombres']:
                hijo = BonificacionFamiliar(
                    empleado_id=empleado.id,
                    nombre=nombre,
                    fecha_nacimiento=date(2015, randint(1, 12), randint(1, 28)),
                    tipo_hijo=TipoHijoEnum.HIJO,
                    activo=True
                )
                db.session.add(hijo)
            
            monto = Decimal('60000') * len(hijos_data[i]['nombres'])
            print(f"   ✅ {empleado.nombre}: {len(hijos_data[i]['nombres'])} hijo(s) (₲{monto:,.0f}/mes)")
    
    db.session.commit()


# ===================== MAIN =====================

def main():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("🧹 LIMPIEZA Y GENERACIÓN DE DATOS DE PRUEBA - NOVIEMBRE 2025")
        print("="*80)
        
        # Paso 1: Limpiar
        if not limpiar_base_datos():
            print("\n❌ Error en la limpieza. Abortando.")
            return
        
        # Obtener empleados activos
        empleados = Empleado.query.filter_by(estado='Activo').all()
        
        if len(empleados) == 0:
            print("\n❌ No hay empleados activos. Por favor crea empleados primero.")
            return
        
        print("\n" + "="*80)
        print("🎨 PASO 2: GENERANDO DATOS DE NOVIEMBRE 2025")
        print("="*80)
        
        # Paso 2: Generar vacaciones PRIMERO (para que asistencias las respeten)
        generar_vacaciones(empleados)
        
        # Paso 3: Generar asistencias
        generar_asistencias_noviembre(empleados)
        
        # Paso 4: Generar sanciones (basadas en asistencias)
        generar_sanciones(empleados)
        
        # Paso 5: Generar anticipos
        generar_anticipos(empleados)
        
        # Paso 6: Generar ingresos extras
        generar_ingresos_extras(empleados)
        
        # Paso 7: Generar permisos
        generar_permisos(empleados)
        
        # Paso 8: Generar bonificaciones familiares
        generar_bonificaciones_familiares(empleados)
        
        # Resumen
        print("\n" + "="*80)
        print("✅ DATOS DE PRUEBA GENERADOS EXITOSAMENTE")
        print("="*80)
        
        # Contar registros creados
        asistencias = db.session.query(Asistencia).count()
        vacaciones = db.session.query(Vacacion).count()
        sanciones = db.session.query(Sancion).count()
        anticipos = db.session.query(Anticipo).count()
        ingresos = db.session.query(IngresoExtra).count()
        horas = db.session.query(HorasExtra).count()
        permisos = db.session.query(Permiso).count()
        bonificaciones = db.session.query(BonificacionFamiliar).count()
        
        print(f"\n📊 RESUMEN:")
        print(f"   - {asistencias} registros de asistencia")
        print(f"   - {vacaciones} períodos de vacaciones")
        print(f"   - {sanciones} sanciones")
        print(f"   - {anticipos} anticipos pendientes de aplicar")
        print(f"   - {ingresos} ingresos extras")
        print(f"   - {horas} horas extra")
        print(f"   - {permisos} permisos")
        print(f"   - {bonificaciones} bonificaciones familiares")
        
        print(f"\n🎯 AHORA PUEDES:")
        print(f"   1. Ir a http://127.0.0.1:5000/rrhh/liquidaciones")
        print(f"   2. Generar liquidación de Noviembre 2025")
        print(f"   3. Verificar que:")
        print(f"      - Anticipos se descuenten automáticamente")
        print(f"      - Sanciones se incluyan en descuentos")
        print(f"      - Bonificaciones familiares se apliquen")
        print(f"      - Ingresos extras se sumen")
        print(f"      - Salarios sean proporcionales a días trabajados")
        print(f"\n💡 NOTA: No se generó liquidación para que puedas demostrar")
        print(f"         el proceso completo en tu presentación.")
        print("\n" + "="*80)


if __name__ == '__main__':
    main()
