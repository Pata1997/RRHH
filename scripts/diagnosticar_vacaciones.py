"""
Script para diagnosticar por qué no se encuentran las vacaciones en la liquidación
"""

import sys
import os
from datetime import date, timedelta
import calendar

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Forzar configuración de producción para PostgreSQL
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from app.models import Empleado, Vacacion, EstadoVacacionEnum, Asistencia
from sqlalchemy import func

app = create_app('production')

with app.app_context():
    print('='*70)
    print('🔍 DIAGNÓSTICO DE VACACIONES')
    print('='*70)
    
    # Buscar empleados con vacaciones en noviembre 2025
    año = 2025
    mes = 11
    primer_dia = date(año, mes, 1)
    ultimo_dia = date(año, mes, calendar.monthrange(año, mes)[1])
    
    print(f'\n📅 Período: {primer_dia} a {ultimo_dia}')
    print(f'   Año: {año}, Mes: {mes}')
    
    # Buscar TODAS las vacaciones de noviembre
    print('\n' + '='*70)
    print('📋 TODAS LAS VACACIONES EN EL SISTEMA')
    print('='*70)
    
    todas_vacaciones = Vacacion.query.all()
    print(f'\nTotal de registros de vacaciones: {len(todas_vacaciones)}')
    
    for vac in todas_vacaciones:
        emp = Empleado.query.get(vac.empleado_id)
        print(f'\n  Empleado: {emp.codigo} - {emp.nombre_completo}')
        print(f'  ID Vacación: {vac.id}')
        print(f'  Año: {vac.año}')
        print(f'  Fecha inicio: {vac.fecha_inicio_solicitud}')
        print(f'  Fecha fin: {vac.fecha_fin_solicitud}')
        print(f'  Estado: {vac.estado}')
        print(f'  Días tomados: {vac.dias_tomados}')
    
    # Buscar vacaciones que deberían aplicar a noviembre
    print('\n' + '='*70)
    print('🔍 VACACIONES QUE DEBERÍAN APLICAR A NOVIEMBRE 2025')
    print('='*70)
    
    vacaciones_noviembre = Vacacion.query.filter(
        Vacacion.fecha_inicio_solicitud <= ultimo_dia,
        Vacacion.fecha_fin_solicitud >= primer_dia
    ).all()
    
    print(f'\nEncontradas: {len(vacaciones_noviembre)} vacaciones')
    
    for vac in vacaciones_noviembre:
        emp = Empleado.query.get(vac.empleado_id)
        print(f'\n  ✓ Empleado: {emp.codigo} - {emp.nombre_completo}')
        print(f'    ID Vacación: {vac.id}')
        print(f'    Fecha inicio: {vac.fecha_inicio_solicitud}')
        print(f'    Fecha fin: {vac.fecha_fin_solicitud}')
        print(f'    Estado: {vac.estado} (¿Es APROBADA? {vac.estado == EstadoVacacionEnum.APROBADA})')
        
        # Calcular días hábiles de vacación
        inicio = max(vac.fecha_inicio_solicitud, primer_dia)
        fin = min(vac.fecha_fin_solicitud, ultimo_dia)
        fecha_temp = inicio
        dias_habiles_vac = 0
        while fecha_temp <= fin:
            if fecha_temp.weekday() < 5:
                dias_habiles_vac += 1
            fecha_temp += timedelta(days=1)
        
        print(f'    Días hábiles de vacación en noviembre: {dias_habiles_vac}')
        
        # Verificar asistencias en esas fechas
        fecha_temp = inicio
        print(f'\n    📊 Asistencias durante vacaciones:')
        while fecha_temp <= fin:
            if fecha_temp.weekday() < 5:
                asist = Asistencia.query.filter_by(
                    empleado_id=emp.id,
                    fecha=fecha_temp
                ).first()
                
                if asist:
                    print(f'      {fecha_temp} ({fecha_temp.strftime("%A")}): {"✓ Presente" if asist.presente else "✗ Ausente"}')
                else:
                    print(f'      {fecha_temp} ({fecha_temp.strftime("%A")}): Sin registro de asistencia')
            fecha_temp += timedelta(days=1)
    
    # Buscar solo vacaciones APROBADAS
    print('\n' + '='*70)
    print('✅ VACACIONES APROBADAS EN NOVIEMBRE 2025')
    print('='*70)
    
    vacaciones_aprobadas = Vacacion.query.filter(
        Vacacion.estado == EstadoVacacionEnum.APROBADA,
        Vacacion.fecha_inicio_solicitud <= ultimo_dia,
        Vacacion.fecha_fin_solicitud >= primer_dia
    ).all()
    
    print(f'\nEncontradas: {len(vacaciones_aprobadas)} vacaciones aprobadas')
    
    if len(vacaciones_aprobadas) == 0:
        print('\n⚠️  NO HAY VACACIONES APROBADAS EN NOVIEMBRE')
        print('   Esto explica por qué la liquidación no las encuentra.')
        print('\n   Posibles causas:')
        print('   1. Las vacaciones no tienen estado APROBADA')
        print('   2. Las fechas no están en noviembre 2025')
        print('   3. No se crearon vacaciones en el script de generación')
    else:
        for vac in vacaciones_aprobadas:
            emp = Empleado.query.get(vac.empleado_id)
            print(f'\n  ✓ {emp.codigo} - {emp.nombre_completo}')
            print(f'    Del {vac.fecha_inicio_solicitud} al {vac.fecha_fin_solicitud}')
    
    print('\n' + '='*70)
    print('✅ DIAGNÓSTICO COMPLETADO')
    print('='*70)
