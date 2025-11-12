# 🧪 GUÍA: GENERAR DATOS DE PRUEBA

## 🎯 ¿QUÉ HACE?

El script genera datos realistas para probar el sistema:

```
✅ Asistencias: Todo octubre (22 días hábiles) - todos presentes
✅ Descuentos: 3 empleados con descuento manual (10% salario)
✅ Sanciones: 3 empleados con sanciones + descuentos automáticos
```

**Resultado:** 6 empleados listos para generar liquidación de octubre

---

## 🚀 CÓMO EJECUTAR (3 pasos)

### **Paso 1: Abre PowerShell**

En la carpeta del proyecto:

```powershell
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
```

### **Paso 2: Ejecuta el script**

```powershell
python scripts/generar_datos_prueba.py
```

### **Paso 3: Espera el resultado**

Verás algo como:

```
============================================================
GENERADOR DE DATOS DE PRUEBA
============================================================

✓ Encontrados 6 empleados:
  - Juan Pérez (ID: 1)
  - María García (ID: 2)
  - ... (4 más)

📅 Octubre 2025: 22 días hábiles
   Rango: 01/10 - 31/10

📝 Generando asistencias...
   ✓ 132 asistencias creadas (6 × 22 días)

💰 Agregando descuentos a 3 empleados...
   ✓ Juan Pérez: -200,000 Gs. (10% salario)
   ✓ María García: -150,000 Gs. (10% salario)
   ✓ Pedro López: -180,000 Gs. (10% salario)

⚠️  Agregando sanciones a 3 empleados...
   ✓ Ana Martínez: Suspensión (5 días = -333,333.33 Gs.)
   ✓ Luis Gómez: Amonestación (3 días = -200,000 Gs.)
   ✓ Rosa Díaz: Falta grave (2 días = -133,333.33 Gs.)

============================================================
✅ DATOS DE PRUEBA GENERADOS EXITOSAMENTE
============================================================
```

---

## ✅ DESPUÉS DE EJECUTAR

Ahora tienes datos realistas. Prueba esto:

### **1️⃣ Generar liquidación de octubre**

```
Menú → Nómina → Generar
Período: 2025-10
Presiona: Generar
```

**Resultado:** 6 liquidaciones con:
- ✅ Salario base
- ✅ Descuentos manuales (3 empleados)
- ✅ Descuentos por sanciones (3 empleados)
- ✅ Aporte IPS automático
- ✅ Salario neto final

### **2️⃣ Ver liquidación detallada**

```
Menú → Nómina → Liquidaciones
Filtra período: 2025-10
Haz click en un empleado
```

**Verás:**
- Desglose de salario base
- Ingresos extras (si los hay)
- Todos los descuentos (manual + sanciones)
- Aporte IPS
- Total neto

### **3️⃣ Descargar PDF**

```
En la fila del empleado: botón "PDF"
```

### **4️⃣ Probar otros módulos**

```
Menú → Nómina → Registrar Despido
  - Selecciona un empleado
  - Tipo: Injustificado
  - Se genera liquidación automática de despido

Menú → Nómina → Generar Aguinaldo
  - Año: 2025
  - Previsualiza
  - Genera
```

---

## 📊 DETALLES DE LOS DATOS

### Asistencias (Octubre)

```
✓ Todos los días hábiles (lunes a viernes)
✓ Hora entrada: 08:00
✓ Hora salida: 17:00
✓ Todos presentes
✓ Total: 22 días × 6 empleados = 132 asistencias
```

### Descuentos Manuales (Empleados 1-3)

```
Empleado 1: 10% del salario base
Empleado 2: 10% del salario base
Empleado 3: 10% del salario base

(Estos aparecen en liquidación como "Descuentos")
```

### Sanciones (Empleados 4-6)

```
Empleado 4: Suspensión (5 días)
           = 5 × (Salario/30)

Empleado 5: Amonestación (3 días)
           = 3 × (Salario/30)

Empleado 6: Falta grave (2 días)
           = 2 × (Salario/30)

(Los descuentos se crean automáticamente)
```

---

## 🔄 ¿PUEDO EJECUTARLO VARIAS VECES?

**Sí, es seguro:**
- Los descuentos y sanciones se agregan (no duplican)
- Las asistencias se saltan si ya existen
- Puedes ejecutarlo 2-3 veces sin problema

---

## ❌ SI ALGO FALLA

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución:**
```powershell
# Asegúrate de estar en la carpeta correcta
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
ls  # Debería mostrar carpeta "app"
python scripts/generar_datos_prueba.py
```

### Error: "No hay 6 empleados"

**Solución:**
Primero crea 6 empleados en el sistema:
```
Menú → Empleados → Crear
(Repite 6 veces)
```

Luego ejecuta el script.

### Error: "Table 'asistencias' does not exist"

**Solución:**
Necesitas haber ejecutado la migración de despidos primero:
```powershell
python migrations/add_despido_table.py
```

---

## 📝 FLUJO COMPLETO DE PRUEBAS

```
1. Ejecuta: python scripts/generar_datos_prueba.py
   └─ Genera asistencias, descuentos, sanciones

2. Va a: Menú → Nómina → Generar
   └─ Selecciona 2025-10
   └─ Genera liquidaciones con descuentos incluidos

3. Va a: Menú → Nómina → Liquidaciones
   └─ Ve desglose de cada empleado
   └─ Descarga PDF

4. Va a: Menú → Nómina → Registrar Despido
   └─ Prueba registrar despido
   └─ Ve cálculos automáticos

5. Va a: Menú → Nómina → Generar Aguinaldo
   └─ Selecciona 2025
   └─ Previsualiza
   └─ Genera

6. Va a: Menú → Nómina → Aguinaldos
   └─ Ve listado
   └─ Descarga PDFs
```

---

## 💡 TIPS

**Tip 1:** Ejecuta el script primero, luego abre la app

**Tip 2:** Si los números se ven raros en los cálculos, revisa que los 6 empleados tengan salario_base asignado

**Tip 3:** Los PDFs usan datos de la BD, así que asegúrate de generar liquidación primero

**Tip 4:** Puedes ejecutar varias veces sin miedo (es idempotente)

---

## ✨ RESUMEN RÁPIDO

```
1. PowerShell
2. cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
3. python scripts/generar_datos_prueba.py
4. Espera ✓ DATOS GENERADOS
5. Ve a: Menú → Nómina → Generar
6. Período: 2025-10
7. ¡Listo a probar!
```

---

**¡A probar el sistema! 🚀**
