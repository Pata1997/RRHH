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

## 📊 FÓRMULA DE CÁLCULO

```
┌─────────────────────────────────────────────────┐
│ Días trabajados en año = Fecha pago - 1 Enero   │
├─────────────────────────────────────────────────┤
│ Meses trabajados = Días / 30                    │
├─────────────────────────────────────────────────┤
│ Aguinaldo BRUTO = (Meses / 12) × Salario Base   │
├─────────────────────────────────────────────────┤
│ IPS 9% = Aguinaldo BRUTO × 0.09                 │
├─────────────────────────────────────────────────┤
│ Aguinaldo NETO = Aguinaldo BRUTO - IPS          │
└─────────────────────────────────────────────────┘
```

### **Ejemplo práctico (Año 2025, corte 31 Dic):**

```
Empleado: Juan Pérez
Salario Base: 2,000,000 Gs.
Días trabajados: 365 (año completo)
Meses trabajados: 365 / 30 = 12.17 meses

Aguinaldo BRUTO = (12.17 / 12) × 2,000,000
                = 1.01 × 2,000,000
                = 2,030,000 Gs.

IPS 9% = 2,030,000 × 0.09 = 182,700 Gs.

NETO = 2,030,000 - 182,700 = 1,847,300 Gs.
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
