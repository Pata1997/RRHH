# 🚨 FIX CRÍTICO: Anticipos no se descuentan en liquidación

## ❌ PROBLEMA DETECTADO

### **Bug Crítico en generar_liquidacion()**
```python
# UBICACIÓN: app/routes/rrhh.py línea ~1958

# CÓDIGO ACTUAL (INCORRECTO):
descuentos = db.session.query(func.sum(Descuento.monto)).filter(
    Descuento.empleado_id == empleado.id,
    Descuento.mes == mes,
    Descuento.año == año
).scalar() or Decimal('0')

# ❌ Solo consulta tabla `descuentos`
# ❌ NO consulta tabla `anticipos`
# ❌ Anticipos aprobados NO se descuentan del salario
```

### **Impacto:**
```
EJEMPLO REAL:
- Empleado solicita anticipo: ₲500.000
- RRHH aprueba anticipo → empleado recibe ₲500.000
- Fin de mes: generar_liquidacion()
  - Salario base: ₲3.000.000
  - Descuentos: ₲0 (anticipo NO incluido)
  - Neto: ₲3.000.000
- RESULTADO: Empleado cobró ₲3.500.000 total
- DEBERÍA: ₲2.500.000

PÉRDIDA: ₲500.000 por cada anticipo no descontado
```

---

## ✅ SOLUCIÓN

### **Modificación en `generar_liquidacion()`**

```python
# UBICACIÓN: app/routes/rrhh.py
# Línea aproximada: 1955-1970

# ========================================
# CAMBIO 1: Calcular Descuentos + Anticipos
# ========================================

# CÓDIGO ORIGINAL:
descuentos = db.session.query(func.sum(Descuento.monto)).filter(
    Descuento.empleado_id == empleado.id,
    Descuento.mes == mes,
    Descuento.año == año
).scalar() or Decimal('0')

# 🆕 AGREGAR DESPUÉS:

# Calcular anticipos aprobados del mes que aún no se aplicaron
anticipos_mes = db.session.query(func.sum(Anticipo.monto)).filter(
    Anticipo.empleado_id == empleado.id,
    func.extract('month', Anticipo.fecha_aprobacion) == mes,
    func.extract('year', Anticipo.fecha_aprobacion) == año,
    Anticipo.aprobado == True,
    Anticipo.aplicado == False
).scalar() or Decimal('0')

# Sumar descuentos + anticipos
descuentos_totales = descuentos + anticipos_mes

# ========================================
# CAMBIO 2: Usar descuentos_totales en cálculos
# ========================================

# CAMBIAR (línea ~1968):
# ANTES:
salario_neto = salario_base_ajustado + ingresos_extras + bonificacion_familiar - descuentos - aporte_ips

# DESPUÉS:
salario_neto = salario_base_ajustado + ingresos_extras + bonificacion_familiar - descuentos_totales - aporte_ips

# ========================================
# CAMBIO 3: Crear liquidación con descuentos_totales
# ========================================

# CAMBIAR (línea ~1975):
liquidacion = Liquidacion(
    empleado_id=empleado.id,
    periodo=periodo,
    salario_base=salario_base_ajustado,
    bonificacion_familiar=bonificacion_familiar,
    ingresos_extras=ingresos_extras,
    descuentos=descuentos_totales,  # ← CAMBIAR de `descuentos` a `descuentos_totales`
    aporte_ips=aporte_ips,
    salario_neto=salario_neto,
    dias_trabajados=dias_presentes
)

# ========================================
# CAMBIO 4: Marcar anticipos como aplicados
# ========================================

# AGREGAR después de marcar ingresos_extras y horas_extra como aplicados
# (línea aproximada ~2005):

# Marcar anticipos como aplicados
anticipos_a_aplicar = Anticipo.query.filter(
    Anticipo.empleado_id == empleado.id,
    func.extract('month', Anticipo.fecha_aprobacion) == mes,
    func.extract('year', Anticipo.fecha_aprobacion) == año,
    Anticipo.aprobado == True,
    Anticipo.aplicado == False
).all()

for anticipo in anticipos_a_aplicar:
    anticipo.aplicado = True
    anticipo.fecha_aplicacion = date(año, mes, 1)
```

---

## 📋 CÓDIGO COMPLETO CORREGIDO

```python
# app/routes/rrhh.py - Función generar_liquidacion()
# Sección de cálculo de descuentos (línea ~1955-2010)

# ... código anterior ...

# Calcular descuentos manuales
descuentos = db.session.query(func.sum(Descuento.monto)).filter(
    Descuento.empleado_id == empleado.id,
    Descuento.mes == mes,
    Descuento.año == año
).scalar() or Decimal('0')

# 🆕 NUEVO: Calcular anticipos del mes
anticipos_mes = db.session.query(func.sum(Anticipo.monto)).filter(
    Anticipo.empleado_id == empleado.id,
    func.extract('month', Anticipo.fecha_aprobacion) == mes,
    func.extract('year', Anticipo.fecha_aprobacion) == año,
    Anticipo.aprobado == True,
    Anticipo.aplicado == False
).scalar() or Decimal('0')

# 🆕 NUEVO: Sumar descuentos totales
descuentos_totales = descuentos + anticipos_mes

# Calcular bonificación familiar
fecha_liquidacion = date(año, mes, 1)
bonificacion_familiar = calcular_bonificacion_familiar(empleado.id, fecha_liquidacion)

# Calcular aporte IPS (9.625% sobre salario ajustado + ingresos extras + bonificación)
aporte_ips = (salario_base_ajustado + ingresos_extras + bonificacion_familiar) * Decimal('0.09625')

# Calcular salario neto (USAR descuentos_totales)
salario_neto = salario_base_ajustado + ingresos_extras + bonificacion_familiar - descuentos_totales - aporte_ips

# Crear liquidación (USAR descuentos_totales)
liquidacion = Liquidacion(
    empleado_id=empleado.id,
    periodo=periodo,
    salario_base=salario_base_ajustado,
    bonificacion_familiar=bonificacion_familiar,
    ingresos_extras=ingresos_extras,
    descuentos=descuentos_totales,  # ← CAMBIO
    aporte_ips=aporte_ips,
    salario_neto=salario_neto,
    dias_trabajados=dias_presentes
)

db.session.add(liquidacion)
db.session.flush()

# Marcar ingresos extras como aplicados
ingresos_a_aplicar = IngresoExtra.query.filter(
    IngresoExtra.empleado_id == empleado.id,
    IngresoExtra.mes == mes,
    IngresoExtra.año == año,
    IngresoExtra.estado == 'APROBADO',
    IngresoExtra.aplicado == False
).all()
for ie in ingresos_a_aplicar:
    ie.aplicado = True
    ie.fecha_aplicacion = datetime.utcnow()

# Marcar horas extra como aplicadas
horas_a_aplicar = HorasExtra.query.filter(
    HorasExtra.empleado_id == empleado.id,
    func.extract('year', HorasExtra.fecha) == año,
    func.extract('month', HorasExtra.fecha) == mes,
    HorasExtra.estado == 'APROBADO',
    HorasExtra.aplicado == False
).all()
for he in horas_a_aplicar:
    he.aplicado = True
    he.fecha_aplicacion = datetime.utcnow()

# 🆕 NUEVO: Marcar anticipos como aplicados
anticipos_a_aplicar = Anticipo.query.filter(
    Anticipo.empleado_id == empleado.id,
    func.extract('month', Anticipo.fecha_aprobacion) == mes,
    func.extract('year', Anticipo.fecha_aprobacion) == año,
    Anticipo.aprobado == True,
    Anticipo.aplicado == False
).all()
for anticipo in anticipos_a_aplicar:
    anticipo.aplicado = True
    anticipo.fecha_aplicacion = date(año, mes, 1)

contador += 1

# ... resto del código ...
```

---

## 🔍 AUDITORÍA: Detectar Liquidaciones Afectadas

### **Query SQL para identificar dobles pagos**

```sql
-- Empleados con anticipos aprobados que NO se descontaron
SELECT 
    e.codigo,
    e.nombre_completo,
    l.periodo,
    l.salario_neto as salario_pagado,
    a.monto as anticipo_no_descontado,
    (l.salario_neto - a.monto) as deberia_haber_pagado,
    a.monto as perdida
FROM liquidaciones l
JOIN empleados e ON e.id = l.empleado_id
JOIN anticipos a ON (
    a.empleado_id = l.empleado_id
    AND a.aprobado = TRUE
    AND a.aplicado = FALSE
    AND EXTRACT(YEAR FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 1) AS INT)
    AND EXTRACT(MONTH FROM a.fecha_aprobacion) = CAST(SPLIT_PART(l.periodo, '-', 2) AS INT)
)
ORDER BY l.periodo DESC, e.codigo;
```

### **Resultado esperado:**
```
codigo | nombre_completo | periodo | salario_pagado | anticipo_no_descontado | deberia_haber_pagado | perdida
-------|-----------------|---------|----------------|------------------------|---------------------|--------
E001   | Juan Pérez      | 2025-11 | 3,000,000      | 500,000                | 2,500,000          | 500,000
E015   | Ana García      | 2025-10 | 2,800,000      | 400,000                | 2,400,000          | 400,000
...
```

---

## ✅ VALIDACIÓN POST-FIX

### **Test Case 1: Anticipo Simple**
```python
# Crear empleado
empleado = Empleado(salario_base=3000000)

# Crear asistencias (22 días presentes de 22)
# ... (todas presente=True)

# Crear anticipo
anticipo = Anticipo(
    empleado_id=empleado.id,
    monto=500000,
    aprobado=True,
    fecha_aprobacion=datetime(2025, 11, 15)
)

# Generar liquidación noviembre 2025
liquidacion = generar_liquidacion('2025-11')

# VALIDAR:
assert liquidacion.descuentos == 500000  # ✅ Anticipo incluido
assert liquidacion.salario_neto == (
    3000000  # salario base
    + 0      # ingresos extras
    + 0      # bonificacion familiar
    - 500000 # anticipo
    - (3000000 * 0.09625)  # IPS
)
```

### **Test Case 2: Anticipo + Descuentos**
```python
# Anticipo: 500,000
# Descuento sanción: 200,000
# Total descuentos: 700,000

liquidacion = generar_liquidacion('2025-11')

assert liquidacion.descuentos == 700000
assert liquidacion.salario_neto == (3000000 - 700000 - ips)
```

### **Test Case 3: Anticipo de mes anterior (no debe descontar)**
```python
# Anticipo octubre (aplicado=True, fecha_aplicacion=2025-10-01)
# Liquidación noviembre

liquidacion = generar_liquidacion('2025-11')

# NO debe incluir anticipo de octubre
assert liquidacion.descuentos == 0
```

---

## 📊 IMPACTO ESTIMADO

```
ESCENARIO CONSERVADOR:
- 50 empleados activos
- 20% solicitan anticipos al mes (10 empleados)
- Promedio anticipo: ₲400.000
- Meses con bug activo: 3

PÉRDIDA TOTAL:
10 empleados × ₲400.000 × 3 meses = ₲12.000.000

ESCENARIO REALISTA:
- Si el bug existe desde implementación (6 meses)
- 30% de empleados usan anticipos
- Promedio: ₲500.000

PÉRDIDA TOTAL:
15 empleados × ₲500.000 × 6 meses = ₲45.000.000
```

---

## 🎯 PASOS DE IMPLEMENTACIÓN

### **1. Backup de Base de Datos** (5 minutos)
```bash
# PostgreSQL
pg_dump -U usuario -d rrhh2 > backup_pre_fix_anticipos_$(date +%Y%m%d).sql
```

### **2. Aplicar Cambios en Código** (30 minutos)
- Editar `app/routes/rrhh.py`
- Agregar cálculo de `anticipos_mes`
- Cambiar `descuentos` por `descuentos_totales`
- Agregar marcado de anticipos como aplicados

### **3. Ejecutar Auditoría SQL** (15 minutos)
- Correr query de detección
- Exportar resultados a Excel
- Calcular pérdida total

### **4. Pruebas en Desarrollo** (45 minutos)
- Crear empleado de prueba
- Crear anticipo aprobado
- Generar liquidación
- Verificar descuento correcto
- Verificar `aplicado=True`

### **5. Deployment a Producción** (10 minutos)
```bash
# Actualizar código
git add app/routes/rrhh.py
git commit -m "FIX: Integrar anticipos en cálculo de liquidación"
git push

# Reiniciar aplicación
# (Según tu método de deploy)
```

### **6. Monitoreo Post-Deploy** (1 semana)
- Verificar liquidaciones nuevas incluyen anticipos
- Validar campo `aplicado=True` se actualiza
- Revisar reportes de empleados

---

## 📞 SOPORTE

Si encuentras problemas durante la implementación:

1. **Revisar logs:** `tail -f logs/app.log`
2. **Verificar tabla anticipos existe:** `\d anticipos` en psql
3. **Comprobar relaciones:** `SELECT * FROM anticipos WHERE aprobado=TRUE AND aplicado=FALSE;`
4. **Rollback si es necesario:** Restaurar backup

---

**PRIORIDAD:** 🔴 CRÍTICA  
**IMPACTO:** Alto (pérdida económica directa)  
**COMPLEJIDAD:** Baja (cambio localizado en 1 función)  
**TIEMPO ESTIMADO:** 2 horas (incluyendo auditoría y pruebas)
