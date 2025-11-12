# 🎯 CÓMO EJECUTAR LA MIGRACIÓN - PASO A PASO

## OPCIÓN 1: Windows PowerShell (Recomendado)

### Paso 1: Abre PowerShell
- Presiona: `Windows + R`
- Escribe: `powershell`
- Presiona: `Enter`

### Paso 2: Navega a la carpeta del proyecto
Copia y pega en PowerShell:

```powershell
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
```

Luego presiona `Enter`

### Paso 3: Ejecuta la migración
Copia y pega:

```powershell
python migrations/add_despido_table.py
```

Presiona `Enter`

### Resultado esperado:
Verás esto en pantalla:

```
======================================================================
MIGRACIÓN: Añadiendo tabla despidos y campos en liquidaciones
======================================================================

✓ Conectado a SQLite: instance/rrhh.db

Base de datos detectada: SQLITE

1. Creando tabla 'despidos'...
   ✓ Tabla 'despidos' creada exitosamente

2. Verificando y añadiendo columnas en 'liquidaciones'...
   ✓ Columna 'liquidaciones.despido_id' agregada
   ✓ Columna 'liquidaciones.indemnizacion_monto' agregada
   ✓ Columna 'liquidaciones.aguinaldo_monto' agregada
   ✓ Columna 'liquidaciones.vacaciones_monto' agregada
   ✓ Columna 'liquidaciones.aportes_ips_despido' agregada

3. Verificando relación entre despidos y liquidaciones...
   • SQLite: Relación FK validada en modelo

======================================================================
✓ MIGRACIÓN COMPLETADA EXITOSAMENTE
======================================================================
```

Si ves `✓ MIGRACIÓN COMPLETADA EXITOSAMENTE` → **¡LISTO!** ✅

---

## OPCIÓN 2: Si usas VS Code integrado

### Paso 1: En VS Code
- Presiona: `Ctrl + Ñ` (o `Ctrl + ~`)
- Se abre Terminal en la parte inferior

### Paso 2: Copia y pega
```powershell
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
python migrations/add_despido_table.py
```

### Paso 3: Presiona Enter
Espera a ver `✓ MIGRACIÓN COMPLETADA EXITOSAMENTE`

---

## OPCIÓN 3: Si algo falla (Alternativa)

Si la migración falla, intenta esto:

```powershell
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
python -m migrations.add_despido_table
```

---

## ❌ ERRORES COMUNES Y SOLUCIONES

### Error: "python: The term 'python' is not recognized"

**Solución:**
```powershell
"C:/Users/Informatica 1/Desktop/Proyectos/RRHH2/venv/Scripts/python.exe" migrations/add_despido_table.py
```

### Error: "No such file or directory: 'instance/rrhh.db'"

**Solución:** La BD no existe. Inicia la app primero:
```powershell
python run.py
```
Deja que inicie, luego presiona `Ctrl + C` para detenerla. Después ejecuta la migración.

### Error: "PermissionError"

**Solución:** Cierra la app y cualquier otra conexión a la BD. Luego intenta nuevamente.

---

## ✅ VERIFICACIÓN (OPCIONAL)

Para verificar que funcionó, abre Python en la misma carpeta:

```powershell
python
```

Luego pega:

```python
from app import create_app, db
from app.models import Despido
app = create_app()
with app.app_context():
    print("Tabla despidos existe:", Despido.__tablename__)
exit()
```

Deberías ver: `Tabla despidos existe: despidos`

---

## 🎬 PRÓXIMOS PASOS DESPUÉS DE MIGRACIÓN

Una vez ejecutada la migración exitosamente:

### 1. Inicia la app
```powershell
python run.py
```

### 2. Abre navegador
```
http://localhost:5000
```

### 3. Inicia sesión (usuario RRHH)

### 4. Ve a: Nómina → Registrar Despido

### 5. ¡Prueba el formulario!

---

## 📊 VISUAL: DÓNDE ESTÁ EL SCRIPT

```
c:\Users\Informatica 1\Desktop\Proyectos\RRHH2\
│
├── migrations/
│   ├── __init__.py
│   ├── add_permiso_columns.py
│   ├── add_permiso_columns_pg.py
│   ├── add_descuento_columns.py
│   └── add_despido_table.py          ← ¡ESTE! 👈
│
└── instance/
    └── rrhh.db                        ← Se actualiza aquí
```

---

## 💡 TIPS

- **No cierres PowerShell** durante la ejecución
- **Espera a ver** el mensaje `✓ MIGRACIÓN COMPLETADA EXITOSAMENTE`
- Si tarda más de 30 segundos, es normal, espera
- **No necesitas borrar nada**, el script es seguro (no elimina datos)

---

## ✨ LISTO

Una vez ejecutes:

```powershell
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
python migrations/add_despido_table.py
```

Y veas:

```
✓ MIGRACIÓN COMPLETADA EXITOSAMENTE
```

**¡TODO FUNCIONA!** 🎉

---

**¿Queda claro? Ejecuta el comando y avísame si hay algún problema.** 👍
