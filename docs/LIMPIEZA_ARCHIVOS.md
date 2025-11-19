# 🗂️ Gestión de Archivos del Proyecto RRHH2

## ✅ Archivos ESENCIALES (MANTENER)

### 📁 Raíz del Proyecto
```
✅ .env                          # Configuración de base de datos (NO SUBIR A GIT)
✅ .env.example                  # Plantilla de variables de entorno
✅ requirements.txt              # Dependencias de Python
✅ run.py                        # Punto de entrada de la aplicación
✅ README.md                     # Documentación principal (ACTUALIZADO)
```

### 📁 Carpetas Esenciales
```
✅ app/                          # Código de la aplicación
✅ docs/                         # Documentación técnica
✅ instance/                     # Base de datos SQLite (desarrollo)
✅ scripts/                      # Scripts de mantenimiento y auditoría
✅ sql/                          # Queries SQL de auditoría
✅ tests/                        # Pruebas unitarias
✅ migrations/                   # Migraciones aplicadas (historial)
✅ venv/                         # Entorno virtual (NO SUBIR A GIT)
```

---

## 🗑️ Archivos a ELIMINAR (Ya no necesarios)

### Scripts Obsoletos de Migración
```
❌ check_permisos.py             # Script temporal de verificación
❌ check_routes.py               # Script temporal de verificación
❌ clean_database.py             # Script de limpieza (peligroso)
❌ fix_bonificaciones_paths.py   # Fix temporal ya aplicado
❌ fix_permiso_path.py           # Fix temporal ya aplicado
❌ grant_permissions.py          # Script temporal de permisos
❌ ver_rutas.py                  # Script de debugging temporal
```

### Archivos de Instalación Obsoletos
```
❌ instalar_y_ejecutar.bat       # Script batch desactualizado
❌ instalar_y_ejecutar.sh        # Script shell desactualizado
   (Motivo: No están actualizados con nuevas dependencias)
```

### Scripts de Migración Específicos (Ya Aplicados)
```
⚠️ migrate_to_postgres.py        # Migración a PostgreSQL (si ya migraste)
⚠️ init_database.py              # Inicialización inicial (si ya está creada)
⚠️ init_despidos.py              # Inicialización despidos (si ya está)
```

### Documentación Obsoleta
```
⚠️ MODELOS_NUEVOS_PARA_AGREGAR.txt  # Lista de tareas (completada)
⚠️ mover_docs.ps1                    # Script temporal PowerShell
```

### Archivos de Base de Datos Temporal
```
⚠️ rrhh_dev.db                    # SQLite de desarrollo (si usas PostgreSQL)
   (Mantener solo si necesitas pruebas sin PostgreSQL)
```

---

## 📂 SCRIPTS - Clasificación Detallada

### ✅ MANTENER - Scripts Útiles
```
✅ scripts/auditoria_anticipos.py         # Auditoría de anticipos crítica
✅ scripts/verificar_anticipo.py          # Verificación de anticipo específico
✅ scripts/generar_datos_prueba.py        # Genera datos de prueba
✅ scripts/test_liquidaciones.py          # Pruebas de liquidaciones
✅ scripts/auto_renew_contracts.py        # Renovación automática de contratos
```

### ⚠️ EVALUAR - Scripts de Propósito Específico
```
⚠️ scripts/regenerar_liquidacion_carlos.py   # Script específico de testing
   → ELIMINAR si solo fue para pruebas puntuales

⚠️ scripts/clean_and_seed.py                 # Limpia y recrea datos
   → MANTENER si necesitas resetear entorno de desarrollo
   → ELIMINAR si ya está estable

⚠️ scripts/exec_sql_sqlalchemy.py            # Ejecuta SQL vía SQLAlchemy
   → MANTENER si ejecutas queries manuales frecuentemente
   → ELIMINAR si no lo usas

⚠️ scripts/migrate_add_empleado_fields.py    # Migración específica
⚠️ scripts/migrate_ips_campos.py             # Migración IPS
⚠️ scripts/migrate_ips_direct.py             # Migración IPS directa
⚠️ scripts/run_migration_empleado_app.py     # Ejecutor de migración
⚠️ scripts/scrp_actualizacion.py             # Script de actualización
   → TODOS estos: MANTENER en migrations/ como historial
   → Pero NO necesitas ejecutarlos nuevamente
```

---

## 📋 MIGRATIONS - Clasificación

### ✅ MANTENER TODAS (Como Historial)
Las migraciones son historial de cambios en la BD. **NO eliminar**, aunque ya estén aplicadas:

```
✅ migrations/add_anticipos.py
✅ migrations/add_anticipo_rechazo.py
✅ migrations/add_asistencia_eventos.py
✅ migrations/add_bonificacion_familiar.py
✅ migrations/add_contrato_variables.py
✅ migrations/add_descuentos_columns.py
✅ migrations/add_descuento_columns.py
✅ migrations/add_despido_table.py
✅ migrations/add_empresa.py
✅ migrations/add_horas_ingresos.py
✅ migrations/add_justificacion_asistencia.py
✅ migrations/add_new_models_pg.py
✅ migrations/add_permiso_columns.py
✅ migrations/add_permiso_columns_pg.py
✅ migrations/add_postulantes_columns.py
✅ migrations/limpieza_total_bonificacion.py
✅ migrations/recreate_bonificacion_familiar.py
✅ migrations/recreate_bonificacion_postgres.py
✅ migrations/rename_metadata_to_detalles.py
```

**Razón:** Son el historial de evolución del esquema de base de datos.

---

## 📖 DOCUMENTACIÓN

### ✅ MANTENER
```
✅ docs/IMPLEMENTACION_COMPLETA.md
✅ docs/ANALISIS_LIQUIDACION_COMPLETO.md
✅ docs/FIX_ANTICIPOS_LIQUIDACION.md
✅ docs/RESUMEN_EJECUTIVO_AUDITORIA.md
✅ README.md (ACTUALIZADO)
✅ SETUP_POSTGRESQL.md
✅ MIGRACION_GUIA.md
```

### ⚠️ EVALUAR
```
⚠️ CLASIFICACION_SIMPLIFICADA.md
   → Si ya no se usa, ELIMINAR

⚠️ INSTALACION_BONIFICACION_FAMILIAR.md
   → Si ya está instalada y documentada en otro lugar, ELIMINAR
```

---

## 🎯 COMANDOS DE LIMPIEZA

### Eliminar Archivos Obsoletos (PowerShell)
```powershell
# ⚠️ PRECAUCIÓN: Revisa antes de ejecutar

# Eliminar scripts temporales
Remove-Item check_permisos.py
Remove-Item check_routes.py
Remove-Item clean_database.py
Remove-Item fix_bonificaciones_paths.py
Remove-Item fix_permiso_path.py
Remove-Item grant_permissions.py
Remove-Item ver_rutas.py

# Eliminar instaladores obsoletos
Remove-Item instalar_y_ejecutar.bat
Remove-Item instalar_y_ejecutar.sh

# Eliminar documentación temporal
Remove-Item MODELOS_NUEVOS_PARA_AGREGAR.txt
Remove-Item mover_docs.ps1

# (OPCIONAL) Eliminar SQLite si usas solo PostgreSQL
Remove-Item rrhh_dev.db

# (OPCIONAL) Eliminar scripts de migración ya aplicados si no los necesitas
Remove-Item init_database.py
Remove-Item init_despidos.py
Remove-Item migrate_to_postgres.py

# (OPCIONAL) Eliminar script de testing específico
Remove-Item scripts/regenerar_liquidacion_carlos.py
```

### Limpieza Segura (Crear backup primero)
```powershell
# 1. Crear carpeta de backup
New-Item -ItemType Directory -Path "..\RRHH2_backup_obsoletos"

# 2. Mover archivos obsoletos al backup (en vez de eliminar)
Move-Item check_permisos.py ..\RRHH2_backup_obsoletos\
Move-Item check_routes.py ..\RRHH2_backup_obsoletos\
Move-Item fix_bonificaciones_paths.py ..\RRHH2_backup_obsoletos\
Move-Item fix_permiso_path.py ..\RRHH2_backup_obsoletos\
Move-Item grant_permissions.py ..\RRHH2_backup_obsoletos\
Move-Item ver_rutas.py ..\RRHH2_backup_obsoletos\
Move-Item instalar_y_ejecutar.bat ..\RRHH2_backup_obsoletos\
Move-Item instalar_y_ejecutar.sh ..\RRHH2_backup_obsoletos\
Move-Item MODELOS_NUEVOS_PARA_AGREGAR.txt ..\RRHH2_backup_obsoletos\
Move-Item mover_docs.ps1 ..\RRHH2_backup_obsoletos\

# 3. Si todo funciona bien después de 1 semana, eliminar backup
# Remove-Item -Recurse ..\RRHH2_backup_obsoletos\
```

---

## 📁 ESTRUCTURA FINAL RECOMENDADA

```
RRHH2/
├── .env                          ✅ Configuración
├── .env.example                  ✅ Plantilla
├── requirements.txt              ✅ Dependencias (ACTUALIZADO)
├── run.py                        ✅ Entrada
├── README.md                     ✅ Doc principal (ACTUALIZADO)
├── SETUP_POSTGRESQL.md           ✅ Setup BD
├── MIGRACION_GUIA.md             ✅ Guía migración
│
├── app/                          ✅ Código aplicación
├── docs/                         ✅ Documentación técnica
├── instance/                     ✅ Instancia local
├── migrations/                   ✅ Historial migraciones
├── scripts/                      ✅ Scripts útiles (limpiados)
│   ├── auditoria_anticipos.py    ✅
│   ├── verificar_anticipo.py     ✅
│   ├── generar_datos_prueba.py   ✅
│   ├── test_liquidaciones.py     ✅
│   └── auto_renew_contracts.py   ✅
├── sql/                          ✅ Queries auditoría
│   └── auditoria_anticipos.sql   ✅
├── tests/                        ✅ Pruebas
└── venv/                         ✅ Entorno virtual
```

---

## ⚡ RESUMEN EJECUTIVO

### Archivos a Eliminar (Seguros)
1. ❌ `check_permisos.py`
2. ❌ `check_routes.py`
3. ❌ `clean_database.py`
4. ❌ `fix_bonificaciones_paths.py`
5. ❌ `fix_permiso_path.py`
6. ❌ `grant_permissions.py`
7. ❌ `ver_rutas.py`
8. ❌ `instalar_y_ejecutar.bat`
9. ❌ `instalar_y_ejecutar.sh`
10. ❌ `MODELOS_NUEVOS_PARA_AGREGAR.txt`
11. ❌ `mover_docs.ps1`
12. ❌ `scripts/regenerar_liquidacion_carlos.py` (script temporal de testing)

### Total a Eliminar: **12 archivos** 🗑️

### Mantener Todo lo Demás: **migrations/**, **app/**, **docs/**, **scripts/ útiles**
