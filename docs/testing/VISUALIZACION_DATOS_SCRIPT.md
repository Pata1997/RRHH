# 🎬 VISUALIZACIÓN: QUÉ GENERA EL SCRIPT

## 📊 ANTES vs DESPUÉS

### ANTES (Base de datos vacía de asistencias/descuentos)

```
EMPLEADO          ASISTENCIAS  DESCUENTOS  SANCIONES
─────────────────────────────────────────────────────
Juan Pérez        0            0           0
María García      0            0           0
Pedro López       0            0           0
Ana Martínez      0            0           0
Luis Gómez        0            0           0
Rosa Díaz         0            0           0
```

### DESPUÉS (Script ejecutado)

```
EMPLEADO          ASISTENCIAS  DESCUENTOS  SANCIONES
─────────────────────────────────────────────────────
Juan Pérez        22 días      ✓ 1         0
María García      22 días      ✓ 1         0
Pedro López       22 días      ✓ 1         0
Ana Martínez      22 días      0           ✓ Suspensión (5 días)
Luis Gómez        22 días      0           ✓ Amonestación (3 días)
Rosa Díaz         22 días      0           ✓ Falta grave (2 días)
```

---

## 📅 OCTUBRE 2025 (Calendario)

```
       OCTUBRE 2025
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31

Días hábiles: 22 (lunes a viernes)
Script crea: 22 asistencias × 6 empleados = 132 registros
```

---

## 💰 DESCUENTOS MANUALES (Empleados 1-3)

### Juan Pérez

```
Salario Base: 2,000,000 Gs.
Descuento: 10% = 200,000 Gs.

En la liquidación de octubre verás:
Salario base:      2,000,000
Descuentos:        - 200,000  ← Script lo crea
Aporte IPS:        - 192,500
───────────────────────────────
Salario neto:      1,607,500
```

### María García

```
Salario Base: 1,500,000 Gs.
Descuento: 10% = 150,000 Gs.

Salario base:      1,500,000
Descuentos:        - 150,000  ← Script lo crea
Aporte IPS:        - 144,375
───────────────────────────────
Salario neto:      1,205,625
```

### Pedro López

```
Salario Base: 1,800,000 Gs.
Descuento: 10% = 180,000 Gs.

Salario base:      1,800,000
Descuentos:        - 180,000  ← Script lo crea
Aporte IPS:        - 173,250
───────────────────────────────
Salario neto:      1,446,750
```

---

## ⚠️ SANCIONES (Empleados 4-6)

### Ana Martínez - Suspensión (5 días)

```
Salario Base: 2,000,000 Gs.
Salario diario: 2,000,000 / 30 = 66,666.67 Gs.
Días sanción: 5
Total sanción: 5 × 66,666.67 = 333,333.33 Gs.

En la liquidación de octubre verás:
Salario base:      2,000,000
Descuentos:        - 333,333  ← Script crea automático por sanción
Aporte IPS:        - 159,725
───────────────────────────────
Salario neto:      1,506,942

Además, en sanciones:
┌────────────────────────────────┐
│ Tipo: Suspensión               │
│ Motivo: Prueba de sanción      │
│ Fecha: 15/10/2025              │
│ Monto: 333,333.33 Gs.          │
└────────────────────────────────┘
```

### Luis Gómez - Amonestación (3 días)

```
Salario Base: 1,600,000 Gs.
Salario diario: 1,600,000 / 30 = 53,333.33 Gs.
Días sanción: 3
Total sanción: 3 × 53,333.33 = 160,000 Gs.

En la liquidación de octubre verás:
Salario base:      1,600,000
Descuentos:        - 160,000  ← Script crea automático
Aporte IPS:        - 138,400
───────────────────────────────
Salario neto:      1,301,600
```

### Rosa Díaz - Falta Grave (2 días)

```
Salario Base: 1,400,000 Gs.
Salario diario: 1,400,000 / 30 = 46,666.67 Gs.
Días sanción: 2
Total sanción: 2 × 46,666.67 = 93,333.33 Gs.

En la liquidación de octubre verás:
Salario base:      1,400,000
Descuentos:        - 93,333   ← Script crea automático
Aporte IPS:        - 125,707
───────────────────────────────
Salario neto:      1,180,960
```

---

## 📋 ESTRUCTURA EN BD

### Tabla: asistencias (132 registros)

```
id | empleado_id | fecha      | hora_entrada | hora_salida | presente
────────────────────────────────────────────────────────────────────
1  | 1           | 2025-10-01 | 08:00:00     | 17:00:00    | 1
2  | 1           | 2025-10-02 | 08:00:00     | 17:00:00    | 1
...
23 | 2           | 2025-10-01 | 08:00:00     | 17:00:00    | 1
...
132| 6           | 2025-10-31 | 08:00:00     | 17:00:00    | 1
```

### Tabla: descuentos (6 registros - 3 manuales + 3 de sanciones)

```
id | empleado_id | tipo             | monto      | mes | año  | origen_tipo
──────────────────────────────────────────────────────────────────────────
1  | 1           | Descuento Manual | 200000.00  | 10  | 2025 | manual
2  | 2           | Descuento Manual | 150000.00  | 10  | 2025 | manual
3  | 3           | Descuento Manual | 180000.00  | 10  | 2025 | manual
4  | 4           | Sanción - Susp   | 333333.33  | 10  | 2025 | sancion
5  | 5           | Sanción - Amond  | 160000.00  | 10  | 2025 | sancion
6  | 6           | Sanción - Falta  | 93333.33   | 10  | 2025 | sancion
```

### Tabla: sanciones (3 registros)

```
id | empleado_id | tipo_sancion | motivo            | fecha      | monto
──────────────────────────────────────────────────────────────────────
1  | 4           | Suspensión   | Prueba de sanción | 2025-10-15 | 0
2  | 5           | Amonestación | Prueba de sanción | 2025-10-15 | 0
3  | 6           | Falta grave  | Prueba de sanción | 2025-10-15 | 0
```

---

## 🎬 FLUJO VISUAL: SCRIPT EJECUTADO

```
START
  │
  ├─→ [Lee 6 empleados de BD]
  │     └─ Juan, María, Pedro, Ana, Luis, Rosa
  │
  ├─→ [Genera asistencias OCTUBRE]
  │     ├─ Del 01/10 al 31/10
  │     ├─ Solo días hábiles (lunes-viernes)
  │     ├─ 22 días × 6 empleados = 132 registros
  │     └─ Todos presentes (08:00-17:00)
  │
  ├─→ [Descuentos MANUALES para empleados 1-3]
  │     ├─ Juan: 200,000 (10% salario)
  │     ├─ María: 150,000 (10% salario)
  │     └─ Pedro: 180,000 (10% salario)
  │
  ├─→ [Sanciones + Descuentos automáticos para 4-6]
  │     ├─ Ana: Suspensión (5 días)
  │     │         └─ Crea descuento automático
  │     ├─ Luis: Amonestación (3 días)
  │     │         └─ Crea descuento automático
  │     └─ Rosa: Falta grave (2 días)
  │             └─ Crea descuento automático
  │
  ├─→ [Guarda todo en BD]
  │
  └─→ [Muestra resumen]
       ✓ 132 asistencias creadas
       ✓ 3 descuentos manuales
       ✓ 3 sanciones + 3 descuentos automáticos

END
```

---

## 🔍 QUÉ VES DESPUÉS EN LA APP

### En Menú → Nómina → Generar (Período: 2025-10)

```
La app automáticamente:
1. Suma salario_base de cada empleado
2. Busca descuentos de ese mes
3. Suma los descuentos manuales + sanciones
4. Calcula IPS 9%
5. Calcula salario neto

Resultado en tabla:
┌─────────────┬─────────┬───────────┬───────┬──────────┐
│ Empleado    │ Base    │ Desctos   │ IPS   │ Neto     │
├─────────────┼─────────┼───────────┼───────┼──────────┤
│ Juan        │ 2.0M    │ -200k     │ -193k │ 1,607.5k │
│ María       │ 1.5M    │ -150k     │ -144k │ 1,205.6k │
│ Pedro       │ 1.8M    │ -180k     │ -173k │ 1,446.7k │
│ Ana         │ 2.0M    │ -333k     │ -160k │ 1,506.9k │
│ Luis        │ 1.6M    │ -160k     │ -138k │ 1,301.6k │
│ Rosa        │ 1.4M    │ -93k      │ -126k │ 1,180.9k │
└─────────────┴─────────┴───────────┴───────┴──────────┘
```

### En Menú → Nómina → Liquidaciones (2025-10)

Haces click en un empleado (ej: Juan):

```
LIQUIDACIÓN DE OCTUBRE
─────────────────────────────────
Empleado: Juan Pérez
Período: 2025-10
Días trabajados: 22 (octubre)

RUBROS:
  Salario base:        2,000,000 Gs.
  Ingresos extras:           0 Gs.
  Descuentos:         -200,000 Gs.  ← Script creó esto
  Aporte IPS 9.625%:  -192,500 Gs.
  ─────────────────────────────
  SALARIO NETO:      1,607,500 Gs.

[Descargar PDF]
```

---

## ✨ RESUMIDO: QUÉ HACE EL SCRIPT

```
Entrada:
- 6 empleados existentes en BD

Salida:
- 132 asistencias (22 días × 6 empleados)
- 6 descuentos (3 manuales + 3 por sanciones)
- 3 sanciones

Para que puedas probar:
- Liquidaciones mensuales (con descuentos incluidos)
- Despidos (elegir un empleado)
- Aguinaldos (calcular para todo el año)
- PDFs (descargar recibos)
```

---

**¡Listo para ver datos realistas en acción!** 🚀
