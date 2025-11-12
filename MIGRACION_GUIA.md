# 🚀 Guía de Migración a PostgreSQL

## Paso 1: Verificar variables de entorno

Asegúrate de que tu archivo `.env` en la raíz del proyecto tiene la conexión a PostgreSQL:

```
DATABASE_URL=postgresql://user:password@localhost:5432/rrhh_db
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=tu_contraseña
PGDATABASE=rrhh_db
```

O si usas solo `DATABASE_URL`, la migración extraerá los datos automáticamente.

## Paso 2: Ejecutar la migración

Abre PowerShell en la raíz del proyecto (donde está `run.py`) y ejecuta:

```powershell
# Activa el entorno virtual (si no está ya activado)
.\venv\Scripts\Activate.ps1

# Ejecuta el script de migración
python migrations\add_new_models_pg.py
```

## Paso 3: Resultado esperado

Verás en la consola algo como:

```
🔌 Conectando a PostgreSQL: postgres@localhost:5432/rrhh_db

📋 [1/6] Verificando columna sanciones.justificativo_archivo...
  → Añadiendo columna justificativo_archivo a sanciones...
  ✓ Columna justificativo_archivo en sanciones añadida

💾 [2/6] Verificando tabla detalles_liquidacion...
  → Creando tabla detalles_liquidacion...
  ✓ Tabla detalles_liquidacion creada

... (más tablas)

✅ ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!
```

## Paso 4: Reiniciar la aplicación Flask

Una vez completada la migración, reinicia tu app Flask:

```powershell
# Si ya está corriendo, presiona CTRL+C y luego:
python run.py
```

## ¿Qué se migra?

✅ **Columna agregada:**
- `sanciones.justificativo_archivo` (VARCHAR 255) - para almacenar ruta a archivos justificativos

✅ **Tablas nuevas creadas:**
1. `detalles_liquidacion` - Desglose de rubros en liquidaciones
2. `familiares_empleados` - Registro de dependientes para bonificación familiar
3. `bonificaciones_familiares` - Bonificación por familiar
4. `postulantes` - Candidatos a vacantes (reclutamiento)
5. `documentos_curriculum` - CVs y documentos de postulantes

## Troubleshooting

### Error: "UndefinedColumn: no existe la columna"

Si aún ves ese error después de ejecutar la migración:
1. Verifica que la migración se ejecutó sin errores.
2. Reinicia la app Flask (CTRL+C y `python run.py`).
3. Intenta acceder nuevamente a `/rrhh/sanciones`.

### Error: "permission denied"

Si la base de datos está protegida:
- Asegúrate de que el usuario PostgreSQL tiene permisos ALTER TABLE.
- Usa un usuario con permisos admin (ej. postgres).

### Error: "connection refused"

Si no conecta a PostgreSQL:
- Verifica que PostgreSQL esté corriendo.
- Verifica las credenciales en `.env`.
- Prueba la conexión manualmente en PowerShell:
  ```powershell
  psql -h localhost -U postgres -d rrhh_db
  ```

## Forzar recreación (si es necesario)

Si algo falla y necesitas empezar de nuevo, puedes limpiar las tablas nuevas (⚠️ PERDERÁS DATOS):

```sql
DROP TABLE IF EXISTS documentos_curriculum CASCADE;
DROP TABLE IF EXISTS bonificaciones_familiares CASCADE;
DROP TABLE IF EXISTS familiares_empleados CASCADE;
DROP TABLE IF EXISTS postulantes CASCADE;
DROP TABLE IF EXISTS detalles_liquidacion CASCADE;
ALTER TABLE sanciones DROP COLUMN IF EXISTS justificativo_archivo;
```

Luego vuelve a ejecutar la migración.

---

**¡Listo! La migración está lista para ejecutarse.**
