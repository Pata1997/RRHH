"""
Script para eliminar solo las liquidaciones de noviembre 2025 y poder regenerarlas
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# Forzar configuración de producción para PostgreSQL
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from app.models import Liquidacion
from sqlalchemy import func

app = create_app('production')

with app.app_context():
    print('='*70)
    print('🗑️  ELIMINANDO LIQUIDACIONES DE NOVIEMBRE 2025')
    print('='*70)
    
    # Buscar liquidaciones de noviembre 2025
    liquidaciones = Liquidacion.query.filter_by(periodo='2025-11').all()
    
    print(f'\n📊 Liquidaciones encontradas: {len(liquidaciones)}')
    
    if len(liquidaciones) == 0:
        print('\n⚠️  No hay liquidaciones de noviembre 2025 para eliminar')
    else:
        print('\nLiquidaciones a eliminar:')
        for liq in liquidaciones:
            print(f'  - {liq.empleado.codigo}: {liq.empleado.nombre_completo} (₲ {liq.salario_neto:,.0f})')
        
        respuesta = input(f'\n¿Confirmar eliminación de {len(liquidaciones)} liquidaciones? (SI/no): ')
        
        if respuesta.strip().upper() == 'SI':
            try:
                # Eliminar liquidaciones
                eliminadas = Liquidacion.query.filter_by(periodo='2025-11').delete()
                db.session.commit()
                
                print(f'\n✅ {eliminadas} liquidaciones eliminadas exitosamente')
                print('\n📝 Ahora puedes regenerar las liquidaciones desde el sistema web:')
                print('   Planillas > Generar Liquidación > Período: 2025-11')
            except Exception as e:
                db.session.rollback()
                print(f'\n❌ Error al eliminar: {e}')
        else:
            print('\n❌ Operación cancelada')
    
    print('\n' + '='*70)
