-- add_empleado_fields_null.sql
-- Anade columnas esenciales para planillas MTESS a la tabla "empleados".
-- Esta version NO establece valores por defecto y deja las filas existentes en NULL.
-- Fecha: 2025-11-14

BEGIN;

ALTER TABLE empleados
  ADD COLUMN IF NOT EXISTS nacionalidad VARCHAR(100);

ALTER TABLE empleados
  ADD COLUMN IF NOT EXISTS ips_numero VARCHAR(50);

ALTER TABLE empleados
  ADD COLUMN IF NOT EXISTS motivo_retiro VARCHAR(255);

COMMIT;

ANALYZE empleados;

