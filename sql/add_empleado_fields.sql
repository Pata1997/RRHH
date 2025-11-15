-- add_empleado_fields.sql
-- Añade columnas esenciales para planillas MTESS a la tabla "empleados".
-- Fecha: 2025-11-14
-- Recomendación: hacer backup antes de ejecutar (usar pg_dump o la opción --backup del script Python).

BEGIN;

-- Agregar columnas (IF NOT EXISTS para seguridad)
ALTER TABLE empleados
  ADD COLUMN IF NOT EXISTS nacionalidad VARCHAR(100) DEFAULT 'Paraguay';

ALTER TABLE empleados
  ADD COLUMN IF NOT EXISTS ips_numero VARCHAR(50);

ALTER TABLE empleados
  ADD COLUMN IF NOT EXISTS motivo_retiro VARCHAR(255);

-- Asegurar que filas existentes tengan valor por defecto en nacionalidad si están NULL
UPDATE empleados
  SET nacionalidad = 'Paraguay'
  WHERE nacionalidad IS NULL;

COMMIT;

-- Actualizar estadísticas
ANALYZE empleados;
