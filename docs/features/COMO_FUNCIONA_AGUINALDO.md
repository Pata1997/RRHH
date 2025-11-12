# 💰 CÓMO SE GENERA EL AGUINALDO AUTOMÁTICAMENTE

## 🎯 Respuesta corta:

**El aguinaldo se calcula automáticamente** cuando registras un despido. No necesitas hacer nada especial. El sistema lo calcula por ti.

---

## 📊 CÓMO FUNCIONA (Paso a paso)

### **Paso 1: Registras un despido**
- Menú → Nómina → **Registrar Despido**
- Seleccionas empleado
- Completas formulario
- Presionas: "Registrar Despido y Generar Liquidación"

### **Paso 2: El sistema calcula automáticamente**
```
Fecha despido = Hoy (11 de noviembre de 2025)

Cálculo del Aguinaldo:
├─ Año de despido = 2025
├─ Fecha inicio año = 1 de enero de 2025
├─ Días trabajados en 2025 = desde 1/1 hasta 11/11
│  └─ Total: 315 días (aprox)
│
├─ Meses trabajados = 315 días / 30 = 10.5 meses
│
└─ AGUINALDO = (10.5 / 12) × Salario Base
    └─ Ejemplo: (10.5 / 12) × 2,000,000 = 1,750,000 Gs.
```

### **Paso 3: Ves el resultado**
- Se abre vista de liquidación
- Muestra tabla con:
  - ✅ Indemnización
  - ✅ **Aguinaldo proporcional** ← Aquí está
  - ✅ Vacaciones no gozadas
  - ✅ Aportes IPS
  - ✅ **TOTAL NETO**

### **Paso 4: Se guarda en BD**
```sql
INSERT INTO liquidaciones (
    aguinaldo_monto,
    indemnizacion_monto,
    vacaciones_monto,
    aportes_ips_despido,
    salario_neto
) VALUES (
    1750000.00,      -- Aguinaldo
    ...
);
```

---

## 🧮 FÓRMULA DEL AGUINALDO (Código Laboral Paraguayo)

```
Aguinaldo Proporcional = (Meses Trabajados en Año / 12) × Salario Base
```

### **Ejemplos prácticos:**

| Mes de Despido | Meses Trabajados | Fórmula | Resultado |
|----------------|------------------|---------|-----------|
| Enero | 1 | (1/12) × 2,000,000 | 166,666.67 Gs. |
| Marzo | 3 | (3/12) × 2,000,000 | 500,000 Gs. |
| Junio | 6 | (6/12) × 2,000,000 | 1,000,000 Gs. |
| Septiembre | 9 | (9/12) × 2,000,000 | 1,500,000 Gs. |
| Noviembre | 11 | (11/12) × 2,000,000 | 1,833,333.33 Gs. |
| Diciembre | 12 | (12/12) × 2,000,000 | 2,000,000 Gs. |

---

## 🔄 VER EL AGUINALDO EN LA LIQUIDACIÓN

### **En la web (después de registrar despido):**

1. Ve a: **Nómina → Registrar Despido**
2. Completa formulario
3. Presiona: "Registrar Despido"
4. **Se abre vista con tabla:**

```
═══════════════════════════════════════════════════
RUBRO                                    MONTO
═══════════════════════════════════════════════════
Indemnización por Antigüedad             $500,000
Aguinaldo (13º Sueldo) Proporcional      $1,833,333.33  ← AQUÍ
Vacaciones No Gozadas                    $200,000
───────────────────────────────────────────────────
Subtotal                                 $2,533,333.33
(-) Aporte IPS (9%)                      -$228,000
═══════════════════════════════════════════════════
TOTAL NETO A PAGAR                       $2,305,333.33
═══════════════════════════════════════════════════
```

5. **Descargar PDF** con el botón abajo

---

## 💾 DÓNDE SE GUARDA EL AGUINALDO

El aguinaldo se almacena en:

### **Base de datos (tabla liquidaciones):**
```sql
SELECT empleado_id, aguinaldo_monto, fecha_generacion
FROM liquidaciones
WHERE despido_id IS NOT NULL;
```

### **Resultado en BD:**
```
empleado_id | aguinaldo_monto | fecha_generacion
─────────────────────────────────────────────────
    5       | 1833333.33      | 2025-11-11
```

### **Archivo PDF:**
- Se genera automáticamente
- Se descarga con nombre: `Liquidacion_Despido_[NombreEmpleado]_[YYYYMMDD].pdf`
- Contiene todos los rubros incluyendo aguinaldo

---

## 🎬 FLUJO COMPLETO: DE PRINCIPIO A FIN

```
┌─────────────────────────────────────────┐
│ 1. USUARIO: Registra Despido            │
│    (Nómina → Registrar Despido)        │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 2. SISTEMA: Calcula automáticamente     │
│    ├─ Indemnización                     │
│    ├─ AGUINALDO ← Aquí                  │
│    ├─ Vacaciones                        │
│    └─ Aportes IPS                       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 3. CREA EN BD:                          │
│    ├─ Registro en tabla DESPIDOS        │
│    ├─ Liquidación en LIQUIDACIONES      │
│    │  └─ aguinaldo_monto: 1,833,333.33 │
│    └─ Registra en BITÁCORA              │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 4. MUESTRA EN WEB:                      │
│    ├─ Vista con detalles                │
│    ├─ Tabla desglosada                  │
│    │  └─ Aguinaldo: $1,833,333.33       │
│    └─ Botón: Descargar PDF              │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 5. USUARIO: Descarga PDF                │
│    ├─ Imprime                           │
│    └─ Archiva                           │
└─────────────────────────────────────────┘
```

---

## ✨ CÓDIGO DETRÁS (Para tu referencia)

### **Función que calcula aguinaldo:**

```python
def calcular_aguinaldo_proporcional(salario_base, fecha_despido):
    """
    Calcula aguinaldo proporcional (13º sueldo).
    """
    año_despido = fecha_despido.year
    fecha_inicio_año = datetime(año_despido, 1, 1).date()
    
    # Días trabajados desde inicio del año
    días_trabajados = (fecha_despido - fecha_inicio_año).days + 1
    meses_trabajados = Decimal(str(días_trabajados)) / Decimal('30')
    
    # Proporción
    aguinaldo = (
        Decimal(str(salario_base)) 
        * meses_trabajados 
        / Decimal('12')
    ).quantize(Decimal('0.01'))
    
    return aguinaldo
```

### **Cómo se usa en liquidación:**

```python
def generar_liquidacion_despido(empleado_id, tipo_despido, ...):
    # ... código previo ...
    
    # AGUINALDO (se calcula automáticamente)
    aguinaldo = calcular_aguinaldo_proporcional(
        empleado.salario_base, 
        fecha_despido
    )
    
    # Se guarda en BD
    liquidacion = Liquidacion(
        aguinaldo_monto=aguinaldo,
        ...
    )
```

---

## ❓ PREGUNTAS FRECUENTES

### **P: ¿Se calcula automáticamente?**
✅ **Sí, 100% automático.** No necesitas hacer nada.

### **P: ¿Se guarda en la BD?**
✅ **Sí**, en tabla `liquidaciones` columna `aguinaldo_monto`.

### **P: ¿Se ve en la web?**
✅ **Sí**, en la vista de liquidación después de registrar despido.

### **P: ¿Se descarga en PDF?**
✅ **Sí**, aparece en el PDF junto con otros rubros.

### **P: ¿Puedo editarlo después?**
❌ **No.** Se calcula en el momento y se guarda. Si necesitas corregir, habría que crear una nueva liquidación.

### **P: ¿Se aplica IPS al aguinaldo?**
✅ **Sí.** El 9% de IPS se aplica a (Indemnización + Aguinaldo + Vacaciones).

---

## 🎯 RESUMEN

```
📌 El aguinaldo se genera AUTOMÁTICAMENTE
   cuando registras un despido.

📌 Se calcula como:
   (Meses trabajados en año / 12) × Salario Base

📌 Se guarda en BD:
   liquidaciones.aguinaldo_monto

📌 Se muestra en:
   ✓ Vista web de liquidación
   ✓ PDF descargable
   ✓ Tabla de rubros desglosados

📌 Tú no necesitas hacer nada:
   El sistema lo hace por ti 🤖
```

---

## 🚀 PRÓXIMO PASO

1. Ejecuta la migración:
   ```powershell
   python migrations/add_despido_table.py
   ```

2. Inicia la app:
   ```powershell
   python run.py
   ```

3. Registra un despido:
   - Menú → Nómina → Registrar Despido
   - Verás el aguinaldo calculado automáticamente ✨

---

**¿Dudas sobre cómo se calcula el aguinaldo? Pregunta.** 👍
