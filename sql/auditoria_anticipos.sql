-- =====================================================
-- SCRIPT DE AUDITORÍA: Anticipos no descontados
-- =====================================================
-- Fecha: 19 de Noviembre 2025
-- Propósito: Detectar liquidaciones con anticipos que no se descontaron

-- =====================================================
-- 1. ANTICIPOS NO DESCONTADOS POR EMPLEADO
-- =====================================================
SELECT 
    e.codigo,
    e.nombre || ' ' || e.apellido as nombre_completo,
    l.periodo,
    l.salario_neto as salario_pagado,
    COALESCE(SUM(a.monto), 0) as anticipos_no_descontados,
    (l.salario_neto - COALESCE(SUM(a.monto), 0)) as deberia_haber_pagado,
    COALESCE(SUM(a.monto), 0) as perdida_empresa
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
ORDER BY l.periodo DESC, e.codigo;

-- =====================================================
-- 2. RESUMEN TOTAL DE PÉRDIDAS
-- =====================================================
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
);

-- =====================================================
-- 3. ANTICIPOS PENDIENTES DE APLICAR (ACTUAL)
-- =====================================================
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
ORDER BY a.fecha_aprobacion DESC;

-- =====================================================
-- 4. PÉRDIDAS POR MES
-- =====================================================
SELECT 
    l.periodo,
    COUNT(DISTINCT l.id) as liquidaciones_con_anticipos,
    COALESCE(SUM(a.monto), 0) as perdida_mes
FROM liquidaciones l
JOIN anticipos a ON (
    a.empleado_id = l.empleado_id
    AND a.aprobado = TRUE
    AND a.aplicado = FALSE
    AND EXTRACT(YEAR FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 1) AS INT)
    AND EXTRACT(MONTH FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 2) AS INT)
)
GROUP BY l.periodo
ORDER BY l.periodo DESC;

-- =====================================================
-- 5. EMPLEADOS CON MÁS ANTICIPOS NO DESCONTADOS
-- =====================================================
SELECT 
    e.codigo,
    e.nombre || ' ' || e.apellido as nombre_completo,
    COUNT(a.id) as cantidad_anticipos,
    SUM(a.monto) as total_anticipos_no_descontados
FROM empleados e
JOIN anticipos a ON a.empleado_id = e.id
WHERE a.aprobado = TRUE
  AND (a.aplicado = FALSE OR a.aplicado IS NULL)
GROUP BY e.id, e.codigo, e.nombre, e.apellido
HAVING COUNT(a.id) > 0
ORDER BY total_anticipos_no_descontados DESC;

-- =====================================================
-- 6. VALIDACIÓN: Sanciones que SÍ crearon descuentos
-- =====================================================
SELECT 
    e.codigo,
    e.nombre || ' ' || e.apellido as nombre_completo,
    s.tipo_sancion,
    s.fecha,
    s.monto as monto_sancion,
    d.monto as monto_descuento,
    d.mes,
    d.año,
    CASE 
        WHEN d.id IS NOT NULL THEN '✅ Descuento creado'
        ELSE '❌ Sin descuento'
    END as estado
FROM sanciones s
JOIN empleados e ON e.id = s.empleado_id
LEFT JOIN descuentos d ON (
    d.origen_tipo = 'sancion' 
    AND d.origen_id = s.id
)
WHERE s.tipo_sancion ILIKE '%suspension%'
ORDER BY s.fecha DESC;

-- =====================================================
-- 7. DESCUENTOS DUPLICADOS (Validación)
-- =====================================================
SELECT 
    empleado_id,
    mes,
    año,
    tipo,
    COUNT(*) as veces_registrado,
    SUM(monto) as monto_total
FROM descuentos
WHERE activo = TRUE
GROUP BY empleado_id, mes, año, tipo
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC;

-- =====================================================
-- INSTRUCCIONES DE USO
-- =====================================================
/*
1. Ejecutar queries en pgAdmin o psql
2. Exportar resultados a Excel para reporte
3. Query #2 te da el TOTAL de pérdidas
4. Query #1 te da el detalle por empleado
5. Query #3 te muestra anticipos que aún se pueden descontar

DESPUÉS DE APLICAR EL FIX:
- Las nuevas liquidaciones descontarán anticipos correctamente
- Los anticipos antiguos quedarán marcados como aplicado=False
- Considerar si ajustar liquidaciones pasadas manualmente
*/
