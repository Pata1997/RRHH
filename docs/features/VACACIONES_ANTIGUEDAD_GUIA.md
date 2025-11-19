# 🏖️ SISTEMA DE VACACIONES POR ANTIGÜEDAD - GUÍA COMPLETA

## 📋 RESUMEN EJECUTIVO

El sistema de vacaciones ha sido **actualizado** para calcular automáticamente los días de vacaciones según la antigüedad del empleado, cumpliendo con el Código Laboral Paraguayo.

### ✅ Cambios Implementados

**ANTES:**
- 15 días fijos para todos los empleados
- Sin consideración de antigüedad
- Gestión manual

**AHORA:**
- **1-5 años de servicio:** 12 días/año
- **5-10 años de servicio:** 18 días/año
- **10+ años de servicio:** 30 días/año
- Cálculo automático
- Acumulación de saldos (hasta 2 años)

---

## 🎯 FUNCIONALIDADES NUEVAS

### 1. Cálculo Automático por Antigüedad

**¿Cómo funciona?**
- El sistema calcula los años de servicio desde `fecha_ingreso`
- Asigna días según la escala legal
- Se actualiza automáticamente cada año

**Ejemplo:**
```
Empleado: Juan Pérez
Fecha ingreso: 15/03/2018
Antigüedad al 2025: 7 años
Días de vacaciones: 18 días/año ✅
```

### 2. Generación Anual Automatizada

**Ruta:** `RRHH > Vacaciones > Generar Período Anual`

**¿Cuándo usar?**
- **Enero de cada año** (inicio del período anual)
- Cuando ingresa un **nuevo empleado**
- Para **actualizar** días según nueva antigüedad

**¿Qué hace?**
1. Recorre todos los empleados activos
2. Calcula días según antigüedad actual
3. Acumula saldos pendientes del año anterior (máx 2 años)
4. Crea o actualiza registros

**Resultado:**
```
✅ Generación completada para 2025:
   - 15 creados
   - 3 actualizados
   - 2 ya existían
```

### 3. Acumulación de Saldos

**Paraguay permite acumular vacaciones no gozadas:**
- Máximo: **2 años** de saldos
- Ejemplo: Empleado con 12 días/año que no tomó vacaciones en 2024:
  ```
  2025 disponibles: 12 (del año) + 12 (saldo 2024) = 24 días
  ```

### 4. Visualización Mejorada

**Lista de Vacaciones:**
- Columna "Antigüedad" muestra años de servicio
- Badge con checkmark indica escala aplicada
- Tooltip explica días por antigüedad

**Detalle por Empleado:**
- Muestra antigüedad completa
- Indica días correspondientes
- Historial año por año

---

## 📖 CASOS DE USO

### Caso 1: Inicio de Año (Generación Masiva)

**Fecha:** Enero 2026

**Pasos:**
1. Ir a: `RRHH > Vacaciones > Generar Período Anual`
2. Seleccionar año: **2026**
3. Click en **"Generar Períodos de Vacaciones"**
4. Verificar resultado

**Resultado esperado:**
- Todos los empleados activos tienen registro para 2026
- Días calculados según antigüedad a dic 2026
- Saldos 2025 acumulados si no fueron gozados

---

### Caso 2: Nuevo Empleado

**Ejemplo:**
- Empleado: María González
- Fecha ingreso: 15/06/2025
- Primer año

**Pasos:**
1. Crear empleado en sistema
2. Ir a: `RRHH > Vacaciones > Generar Período Anual`
3. Seleccionar año: **2025**
4. Sistema genera automáticamente con **12 días** (1-5 años)

**Alternativa automática:**
- Al solicitar vacaciones por primera vez
- Sistema crea registro automáticamente

---

### Caso 3: Empleado Cumple 5 Años

**Ejemplo:**
- Empleado: Carlos Ramírez
- Fecha ingreso: 10/02/2020
- En 2025 cumple 5 años

**¿Qué pasa?**
1. Hasta feb 2025: **12 días/año**
2. A partir de feb 2025: **18 días/año**
3. En generación 2026: automáticamente tendrá **18 días**

**Importante:**
- El sistema calcula antigüedad al 31 dic del año
- Si quieres ajustar inmediatamente:
  1. Ir a generación anual
  2. Regenerar año actual
  3. Marca como "actualizado"

---

### Caso 4: Empleado con 10+ Años

**Ejemplo:**
- Empleado: Roberto Silva
- Fecha ingreso: 05/05/2010
- Antigüedad: 15 años

**Días asignados:** **30 días/año** ✅

**Ventajas:**
- Sistema reconoce automáticamente
- No requiere configuración manual
- Se mantiene mientras sea empleado activo

---

## 🔧 FUNCIONES TÉCNICAS

### calcular_dias_vacaciones_por_antiguedad(empleado, año)

**Descripción:** Calcula días según antigüedad

**Entrada:**
- `empleado`: Objeto Empleado
- `año`: Año de cálculo (opcional, por defecto año actual)

**Salida:** 
- `int`: 12, 18 o 30 días

**Lógica:**
```python
años_servicio = (fecha_calculo - fecha_ingreso).days / 365.25

if años_servicio < 5:  return 12
elif años_servicio < 10: return 18
else: return 30
```

---

### generar_vacaciones_anuales(año, empleado_id)

**Descripción:** Genera períodos anuales masivos

**Entrada:**
- `año`: Año a generar (opcional)
- `empleado_id`: ID específico o None para todos

**Salida:**
```python
{
    'creados': 15,
    'actualizados': 3,
    'ya_existentes': 2,
    'errores': []
}
```

**Comportamiento:**
1. Si no existe registro: **CREA** con días por antigüedad
2. Si existe: **ACTUALIZA** solo si cambió antigüedad
3. Acumula saldos del año anterior (máx 2 años)

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### 1. No Duplica Registros
- Ejecutar varias veces NO genera duplicados
- Solo actualiza si cambió la antigüedad

### 2. Solicitudes Existentes
- Las solicitudes aprobadas/pendientes NO se modifican
- Solo afecta `dias_disponibles` y `dias_pendientes`

### 3. Empleados Inactivos
- Solo procesa empleados con estado **ACTIVO**
- Si un empleado fue despedido, no se regenera

### 4. Años Intermedios
- Si no se generó 2024 y generas 2025:
  - Sistema usa último registro disponible para saldo
  - No crea retroactivamente años pasados

---

## 📊 REPORTES Y VISUALIZACIÓN

### Dashboard de Vacaciones
**Ubicación:** `RRHH > Vacaciones`

**Muestra:**
- Lista completa con antigüedad
- Días disponibles/tomados/pendientes
- Estado de solicitudes
- Acceso a historial individual

### Detalle por Empleado
**Ubicación:** Click en "Ver" en cualquier empleado

**Muestra:**
- Antigüedad actual
- Días correspondientes por antigüedad
- Historial año por año
- Solicitudes pendientes

---

## 🚀 INICIO RÁPIDO

### Primera Vez (Migración)

**Si ya tienes empleados con registros antiguos:**

1. **Generar período actual:**
   ```
   RRHH > Vacaciones > Generar Período Anual
   Año: 2025
   ```

2. **Verificar:**
   - Revisar días asignados por antigüedad
   - Confirmar saldos acumulados
   - Ajustar manualmente si necesario

3. **Documentar:**
   - Anotar empleados con saldos especiales
   - Comunicar cambios al personal

### Cada Año (Enero)

**Rutina anual:**

1. **Primera semana de enero:**
   ```
   RRHH > Vacaciones > Generar Período Anual
   Año: [año actual]
   ```

2. **Comunicar:**
   - Enviar circular con días disponibles
   - Recordar políticas de vacaciones
   - Establecer fechas límite

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Se pierde el saldo si no tomo vacaciones?**
R: No, se acumula hasta 2 años. En el tercer año, el saldo más antiguo vence.

**P: ¿Qué pasa si un empleado pasa de 4 a 5 años en medio del año?**
R: El cálculo se hace al 31 de diciembre. Para el año siguiente tendrá 18 días.

**P: ¿Puedo ajustar manualmente los días?**
R: Sí, puedes editar directamente en la base de datos o crear script personalizado.

**P: ¿El sistema calcula días proporcionales para nuevos empleados?**
R: No, asigna días completos según antigüedad. Para prorrateado, ajusta manualmente.

**P: ¿Se pueden tener escalas diferentes (por ejemplo, 15 días en vez de 12)?**
R: Sí, modifica la función `calcular_dias_vacaciones_por_antiguedad()` en `app/routes/rrhh.py`.

---

## 📝 NOTAS LEGALES

**Base Legal:** Código Laboral del Paraguay

**Artículo 218:**
> Todo trabajador tiene derecho a un período de vacaciones remuneradas 
> después de cada año de trabajo continuo al servicio del mismo empleador.

**Duración (referencia común):**
- 1-5 años: 12 días hábiles
- 5-10 años: 18 días hábiles
- 10+ años: 30 días hábiles

**Nota:** Verificar con normativa específica de tu sector/convenio colectivo.

---

## 🆘 SOPORTE

**Problemas técnicos:**
- Revisar logs en consola Flask
- Verificar cálculo de antigüedad
- Comprobar estado de empleados

**Dudas de uso:**
- Consultar esta guía
- Contactar a RRHH
- Revisar políticas internas

---

✅ **Sistema listo para usar**
📅 **Ejecutar generación anual cada enero**
🎯 **Cálculo automático garantizado**
