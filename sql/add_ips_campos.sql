-- Agregar numero_patronal a la tabla empresas
ALTER TABLE empresas ADD COLUMN numero_patronal VARCHAR(50) NULL;

-- Agregar categoria_ips a la tabla cargos
ALTER TABLE cargos ADD COLUMN categoria_ips VARCHAR(10) DEFAULT '01' NULL;
