# 🎁 AGUINALDOS - IMPLEMENTACIÓN COMPLETA

## ✅ ¿QUÉ SE IMPLEMENTÓ?

Se agregó un **módulo completo de generación de aguinaldos anuales** que permite:

1. **Previsualizar** los cálculos antes de generar
2. **Generar automáticamente** aguinaldos para todos los empleados activos
3. **Consultar y descargar** los aguinaldos en PDF
4. **Evitar duplicados** automáticamente

---

## 🚀 CÓMO USAR (Paso a Paso)

### **Paso 1: Acceder al apartado de Aguinaldos**

1. Inicia sesión con rol **RRHH**
2. Ve a: **Menú → Nómina → Generar Aguinaldo**

### **Paso 2: Seleccionar Año y Fecha de Pago**

En el formulario encontrarás:
- **Año**: Elige el año para el cual generar aguinaldo (ej: 2025)
- **Mes de Pago**: Mes de corte (por defecto: Diciembre)
- **Día de Pago**: Día de corte (por defecto: 31)

### **Paso 3: Previsualizar**

1. Completa los datos
2. Presiona: **"Previsualizar"**
3. Se mostrará una tabla con:
   - Nombre del empleado
   - Meses trabajados en el año
   - Aguinaldo bruto
   - (-) Descuento IPS 9%
   - **Neto a Pagar**
   - **Total consolidado** (suma de todos)

### **Paso 4: Generar Aguinaldos**

1. Si la previsualización es correcta, presiona: **"Generar Aguinaldos"**
2. Se te pedirá confirmación (para evitar acciones accidentales)
3. El sistema genera los registros y muestra resumen:
   - Cantidad de empleados procesados
   - Duplicados evitados (si los hay)
   - Total bruto, total IPS, total neto

### **Paso 5: Consultar y Descargar**

1. Ve a: **Menú → Nómina → Aguinaldos**
2. Filtra por año (filtro arriba)
3. Verás tabla con:
   - Empleado
   - Cédula
   - Cargo
   - Monto aguinaldo
   - Descuentos IPS
   - Neto
4. Presiona **icono PDF** para descargar recibo individual

---

## 📊 FÓRMULA DE CÁLCULO (SEGÚN LEY PARAGUAYA)

### ✅ **Método Correcto Implementado:**

```
┌─────────────────────────────────────────────────────────────────┐
│ PASO 1: Sumar todos los ingresos devengados en el año          │
├─────────────────────────────────────────────────────────────────┤
│ Total Devengado = Σ Salarios + Σ Horas Extras +                │
│                   Σ Comisiones + Σ Bonificaciones Habituales   │
├─────────────────────────────────────────────────────────────────┤
│ PASO 2: Dividir entre 12                                        │
├─────────────────────────────────────────────────────────────────┤
│ Aguinaldo BRUTO = Total Devengado / 12                          │
├─────────────────────────────────────────────────────────────────┤
│ IPS 9% = Aguinaldo BRUTO × 0.09                                 │
├─────────────────────────────────────────────────────────────────┤
│ Aguinaldo NETO = Aguinaldo BRUTO - IPS                          │
└─────────────────────────────────────────────────────────────────┘
```

### **📋 Qué se incluye en el cálculo:**
✅ Salarios mensuales de todas las liquidaciones del año  
✅ Horas extras  
✅ Comisiones  
✅ Bonificaciones habituales  

### **❌ Qué NO se incluye:**
❌ Viáticos no remunerativos  
❌ Aguinaldo del año anterior  
❌ Bonificaciones excepcionales no habituales  

---

### **Ejemplo 1 (Salario Fijo - Año Completo):**

```
Empleado: Juan Pérez
Trabajó todo el año 2025 con salario fijo de 2,500,000 Gs/mes

Total Devengado = 2,500,000 × 12 = 30,000,000 Gs.

Aguinaldo BRUTO = 30,000,000 / 12 = 2,500,000 Gs.

IPS 9% = 2,500,000 × 0.09 = 225,000 Gs.

NETO = 2,500,000 - 225,000 = 2,275,000 Gs.
```

### **Ejemplo 2 (Salarios Variables - Con Extras):**

```
Empleado: María López
Salarios mensuales: 24,000,000 Gs. (año completo)
Horas extras: 3,600,000 Gs.
Comisiones: 6,000,000 Gs.

Total Devengado = 24,000,000 + 3,600,000 + 6,000,000
                = 33,600,000 Gs.

Aguinaldo BRUTO = 33,600,000 / 12 = 2,800,000 Gs.

IPS 9% = 2,800,000 × 0.09 = 252,000 Gs.

NETO = 2,800,000 - 252,000 = 2,548,000 Gs.
```

### **Ejemplo 3 (Sin Liquidaciones Registradas - Fallback):**

```
Si el empleado NO tiene liquidaciones registradas en el sistema,
el sistema calcula proporcionalmente usando el salario base actual:

Empleado: Carlos Gómez
Ingresó el 1 de julio (6 meses trabajados)
Salario Base: 2,000,000 Gs.

Aguinaldo BRUTO = (6 / 12) × 2,000,000 = 1,000,000 Gs.

IPS 9% = 1,000,000 × 0.09 = 90,000 Gs.

NETO = 1,000,000 - 90,000 = 910,000 Gs.
```

---

## 🛡️ CARACTERÍSTICAS IMPORTANTES

### ✓ **Evita duplicados**
- Si ya existe un aguinaldo para ese año y empleado, lo salta automáticamente
- No sobrescribe registros

### ✓ **Maneja casos especiales**
- Empleados contratados a mitad de año → calcula proporcional desde fecha contratación
- Empleados retirados → calcula hasta fecha de retiro (si es antes del corte)
- Empleados inactivos → se excluyen automáticamente

### ✓ **Descuentos automáticos**
- IPS 9% se resta automáticamente del aguinaldo
- Aparece en el recibo como descuento

### ✓ **Auditoría completa**
- Cada generación se registra en la **Bitácora**
- Puedes ver quién, cuándo y qué generó

### ✓ **Exportación**
- Descarga individual PDF para cada empleado
- Usa la función ya existente de descargar recibo

---

## 📝 DÓNDE SE GUARDA

Los aguinaldos se guardan en la tabla **`liquidaciones`** con:

```sql
-- Consulta para ver aguinaldos del año 2025
SELECT 
    empleado.nombre,
    liquidacion.aguinaldo_monto as "Aguinaldo Bruto",
    liquidacion.aportes_ips_despido as "IPS 9%",
    liquidacion.salario_neto as "Neto",
    liquidacion.periodo
FROM liquidaciones
JOIN empleados ON liquidacion.empleado_id = empleado.id
WHERE liquidacion.aguinaldo_monto > 0
  AND liquidacion.periodo LIKE '2025%'
ORDER BY empleado.nombre;
```

---

## ⚡ ACCIONES RÁPIDAS

| Acción | Ruta | Descripción |
|--------|------|-------------|
| Generar | `/rrhh/generar_aguinaldos` | Acceso al formulario |
| Listar | `/rrhh/aguinaldos` | Ver aguinaldos generados |
| Descargar PDF | `/rrhh/liquidaciones/<id>/descargar-pdf` | Recibo individual |

---

## ❓ PREGUNTAS COMUNES

**P: ¿Se puede generar 2 veces el aguinaldo para el mismo año?**
A: No. El sistema detecta si ya existe y lo evita (aparece en columna "Duplicados evitados").

**P: ¿Qué pasa si contrato a alguien el 15 de diciembre?**
A: Se calcula proporcionalmente: desde 15/12 hasta 31/12 (17 días = ~0.56 meses).

**P: ¿Puedo descargar todos los recibos juntos?**
A: Actualmente descargas individualmente. Para masivo, puedes usar un script adicional.

**P: ¿Se incluye a empleados suspendidos o inactivos?**
A: No. Solo empleados con estado "ACTIVO".

**P: ¿Se puede ajustar después?**
A: Actualmente no (revertir automáticamente). Podrías anular el registro y regenerar con datos correctos.

---

## 🔧 COMPONENTES TÉCNICOS

### **Backend (app/routes/rrhh.py)**
- `generar_aguinaldos_anual(año, mes_corte, día_corte)` - Función principal
- `@rrhh_bp.route('/aguinaldos', methods=['GET'])` - Lista aguinaldos
- `@rrhh_bp.route('/generar_aguinaldos', methods=['GET', 'POST'])` - Formulario y generación

### **Frontend**
- `app/templates/rrhh/generar_aguinaldos.html` - Formulario con preview
- `app/templates/rrhh/aguinaldos_listado.html` - Listado de aguinaldos
- **Menú**: Añadido en `base.html` → Nómina → Aguinaldos

### **BD**
- Se usa tabla existente `liquidaciones` (no se modificó schema)
- Campos utilizados: `aguinaldo_monto`, `aportes_ips_despido`, `salario_neto`, `periodo`

---

## ✨ PRÓXIMOS PASOS (OPCIONALES)

Si quieres automatizar aún más:

1. **Programar automáticamente**: Crear tarea Windows Task Scheduler que ejecute generación cada 31 de diciembre
2. **Enviar notificaciones**: Email a RRHH cuando se genera aguinaldo
3. **Reporte consolidado**: Excel con todos los aguinaldos de un año
4. **Reversión masiva**: Botón para deshacer generación si detectas error

---

## 📌 RESUMEN RÁPIDO

```
¿Dónde está? → Menú Nómina → "Generar Aguinaldo"
¿Qué hace?   → Calcula y genera aguinaldos para todos los empleados
¿Cómo?       → Previsualiza → Confirma → Se genera automáticamente
¿Dónde veo?  → Menú Nómina → "Aguinaldos" (listado)
¿Descargar?  → Icono PDF en cada fila
¿Duplicados? → No se generan, se evitan automáticamente
```

---

**¡Listo para usar! 🚀**
