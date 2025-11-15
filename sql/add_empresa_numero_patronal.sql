-- add_empresa_numero_patronal.sql
-- Agrega número patronal a tabla empresas (requerido para planillas IPS/REI)
-- Fecha: 2025-11-15

BEGIN;

ALTER TABLE empresas
  ADD COLUMN IF NOT EXISTS numero_patronal VARCHAR(50);

COMMIT;

ANALYZE empresas;
