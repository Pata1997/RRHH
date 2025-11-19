# ⚡ Instalación de Bonificación Familiar

## 📦 Paso 1: Ejecutar Migración

La migración creará las tablas necesarias y cargará el salario mínimo 2025.

```powershell
# Asegurarse de estar en el directorio del proyecto
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"

# Activar entorno virtual si lo tienes
# .\venv\Scripts\Activate.ps1

# Ejecutar migración
python migrations/add_bonificacion_familiar.py
```

**Salida esperada:**
```
✓ Tabla salarios_minimos creada
✓ Enum tipohijoenum creado
✓ Tabla bonificaciones_familiares creada
✓ Campo bonificacion_familiar agregado a liquidaciones
✓ Salario mínimo 2025 registrado: ₲ 2.798.309
```

## 🔧 Paso 2: Verificar Configuración

### Crear carpeta de uploads (si no existe)

```powershell
New-Item -Path "app\uploads\bonificaciones" -ItemType Directory -Force
```

### Verificar permisos de escritura

La aplicación debe poder escribir en `app/uploads/bonificaciones/`

## ✅ Paso 3: Probar el Sistema

### 1. Acceder al menú

- Iniciar la aplicación: `python run.py`
- Ir a **Nómina** → **Salarios Mínimos**
- Verificar que aparezca el salario 2025

### 2. Registrar primer hijo

- Ir a **RRHH** → **Empleados**
- Click en **Ver** de un empleado activo
- Click en pestaña **Hijos**
- Click en **Agregar Hijo**
- Completar formulario y subir certificado de nacimiento
- Guardar

### 3. Verificar cálculo

- Ir a **Nómina** → **Bonificación Familiar**
- Verificar que aparezca el empleado con:
  - Cantidad de hijos: 1
  - Bonificación mensual: ₲ 139.915 (5% de 2.798.309)

### 4. Generar liquidación de prueba

- Ir a **Planillas** → **Liquidaciones** → **Generar**
- Seleccionar período actual
- Generar liquidaciones
- En el listado, verificar que la columna **Bonif. Familiar** muestre el monto correcto

### 5. Descargar recibo PDF

- Click en botón **PDF** de la liquidación
- Verificar que el recibo incluya la línea:
  ```
  Bonificación Familiar    ₲ 139.915,00
  ```

## 📚 Documentación

Ver documentación completa en:
- `docs/features/BONIFICACION_FAMILIAR_MANUAL.md`

## 🐛 Solución de Problemas

### Error: "table salarios_minimos already exists"

La migración ya fue ejecutada. Verificar con:

```sql
SELECT * FROM salarios_minimos;
```

### Error: "No such table: bonificaciones_familiares"

Ejecutar nuevamente la migración completa.

### Los archivos no se guardan

Verificar:
1. Carpeta `app/uploads/bonificaciones/` existe
2. Permisos de escritura en la carpeta
3. En consola buscar errores relacionados con `secure_filename` o `save()`

### Bonificación no aparece en liquidación

Verificar:
1. El hijo está en estado **Activo** (campo `activo = True`)
2. Existe un salario mínimo vigente para la fecha de liquidación
3. Revisar logs de la aplicación para errores en `calcular_bonificacion_familiar()`

## 🔄 Actualización Anual de Salario Mínimo

Cuando se publique el nuevo salario mínimo:

1. Ir a **Nómina** → **Salarios Mínimos** → **Registrar Nuevo**
2. Completar:
   - **Año:** 2026 (o el que corresponda)
   - **Monto:** Nuevo valor en Guaraníes
   - **Vigencia Desde:** Fecha de inicio (ej: 2026-01-01)
   - **Vigencia Hasta:** Dejar vacío (es el vigente actual)
3. Guardar

**El sistema:**
- Cerrará automáticamente la vigencia del salario anterior
- Usará el nuevo valor para liquidaciones desde la fecha indicada
- Mantendrá el histórico para cálculos retroactivos

## ✨ Próximos Pasos Opcionales

### Automatización de bajas por edad

Crear script para dar de baja automáticamente hijos que cumplen 18 años:

```python
# scripts/auto_baja_hijos_18.py
from app import create_app, db
from app.models import BonificacionFamiliar, TipoHijoEnum
from datetime import date, timedelta

app = create_app()
with app.app_context():
    # Buscar hijos menores de 18 que hoy cumplen 18
    hoy = date.today()
    hace_18_años = hoy - timedelta(days=18*365)
    
    hijos_cumplidos = BonificacionFamiliar.query.filter(
        BonificacionFamiliar.tipo == TipoHijoEnum.MENOR_18,
        BonificacionFamiliar.fecha_nacimiento <= hace_18_años,
        BonificacionFamiliar.activo == True
    ).all()
    
    for hijo in hijos_cumplidos:
        hijo.activo = False
        hijo.fecha_baja = hoy
        hijo.motivo_baja = "Cumplió 18 años - baja automática"
    
    db.session.commit()
    print(f"Dados de baja {len(hijos_cumplidos)} hijos por cumplir 18 años")
```

Ejecutar mensualmente con cron/task scheduler.

## 📞 Contacto

Para dudas o problemas, revisar:
1. Logs de la aplicación
2. Tabla `bitacora` para trazabilidad
3. Documentación completa en `docs/features/`
