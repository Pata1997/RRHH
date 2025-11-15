"""
ips_utils.py
Utilidades para generar planillas IPS/REI
"""

from datetime import date
from decimal import Decimal

# Mapeo de estados de empleado a códigos IPS
ESTADO_IPS_MAPPING = {
    'ACTIVO': '0',         # Activo
    'INACTIVO': '1',       # Inactivo
    'SUSPENDIDO': '2',     # Suspendido
    'JUBILADO': '3',       # Jubilado
}

def get_codigo_situacion(estado_enum_name):
    """
    Convierte EstadoEmpleadoEnum a código de situación IPS.
    
    Args:
        estado_enum_name: Nombre del enum (ej: 'ACTIVO', 'SUSPENDIDO')
    
    Returns:
        str: Código IPS (0, 1, 2, 3)
    """
    return ESTADO_IPS_MAPPING.get(estado_enum_name, '0')


def generar_fila_planilla_ips(empleado, liquidacion, empresa):
    """
    Genera una fila de planilla IPS con todos los campos requeridos.
    
    Columnas exactas según formato REI:
    - Numero Patronal
    - RUC Empresa
    - Razon Social
    - Numero Hoja
    - Cedula
    - Numero Asegurado
    - Apellidos
    - Nombres
    - Dias Trabajados
    - Salario Imponible
    - Categoria (de Cargo.categoria_ips)
    - Codigo Situacion
    - Total Trabajadores (Hoja) - se suma después
    - Total Salario Imponible (Hoja) - se suma después
    - Aporte Empleado
    - Aporte Empleador
    - Total Aporte
    
    Returns:
        dict: Con todos los campos mapeados
    """
    
    # Datos base
    numero_patronal = empresa.numero_patronal or ''
    ruc = empresa.ruc or ''
    razon_social = empresa.razon_social or empresa.nombre or ''
    cedula = empleado.ci or ''
    numero_asegurado = empleado.ips_numero or ''
    apellidos = empleado.apellido or ''
    nombres = empleado.nombre or ''
    
    # Categoría IPS desde el cargo
    categoria = empleado.cargo.categoria_ips if (empleado.cargo and hasattr(empleado.cargo, 'categoria_ips')) else '01'
    
    # Estado (código IPS)
    estado_name = empleado.estado.name if hasattr(empleado.estado, 'name') else str(empleado.estado)
    codigo_situacion = get_codigo_situacion(estado_name)
    
    # Datos de liquidación
    dias_trabajados = liquidacion.dias_trabajados or 0
    salario_imponible = float(liquidacion.salario_base or 0)
    
    # Aportes (calculados desde porcentajes de empresa)
    aporte_empleado = (salario_imponible * float(empresa.porcentaje_ips_empleado or 9)) / 100
    aporte_empleador = (salario_imponible * float(empresa.porcentaje_ips_empleador or 16.5)) / 100
    total_aporte = aporte_empleado + aporte_empleador
    
    return {
        'numero_patronal': numero_patronal,
        'ruc_empresa': ruc,
        'razon_social': razon_social,
        'numero_hoja': 1,  # Se asigna después según paginación
        'cedula': cedula,
        'numero_asegurado': numero_asegurado,
        'apellidos': apellidos,
        'nombres': nombres,
        'dias_trabajados': int(dias_trabajados),
        'salario_imponible': round(salario_imponible, 2),
        'categoria': categoria,
        'codigo_situacion': codigo_situacion,
        'aporte_empleado': round(aporte_empleado, 2),
        'aporte_empleador': round(aporte_empleador, 2),
        'total_aporte': round(total_aporte, 2),
    }
