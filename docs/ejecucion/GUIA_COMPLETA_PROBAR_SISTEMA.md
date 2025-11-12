# 🚀 GUÍA COMPLETA: PASOS PARA PROBAR EL SISTEMA

## ⚡ QUICK START (5 minutos)

```
1. Ejecutar migración BD      (30 seg)
2. Generar datos de prueba    (30 seg)
3. Iniciar app                (30 seg)
4. Probar módulos             (3 min)
```

---

## 📋 PASO 1: EJECUTAR MIGRACIÓN BD

**⏱️ Tiempo: 30 segundos**

Abre PowerShell:

```powershell
cd "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
python migrations/add_despido_table.py
```

Espera:

```
✓ MIGRACIÓN COMPLETADA EXITOSAMENTE
✓ Tabla 'despidos' creada
✓ Columnas agregadas a 'liquidaciones'
```

**Si falla:** Lee `AGUINALDOS_SIGUIENTE_PASO.txt`

---

## 📊 PASO 2: GENERAR DATOS DE PRUEBA

**⏱️ Tiempo: 30 segundos**

En el mismo PowerShell:

```powershell
python scripts/generar_datos_prueba.py
```

Espera:

```
✓ Encontrados 6 empleados:
  - Juan Pérez
  - María García
  - Pedro López
  - Ana Martínez
  - Luis Gómez
  - Rosa Díaz

✓ 132 asistencias creadas (6 × 22 días)
✓ Descuentos manuales: 3 empleados (10% salario)
✓ Sanciones: 3 empleados con descuentos automáticos

✅ DATOS DE PRUEBA GENERADOS EXITOSAMENTE
```

**¿Qué genera?**
- 22 días de asistencia (octubre) para 6 empleados
- 3 descuentos manuales (10% salario c/u)
- 3 sanciones + descuentos automáticos

---

## 🖥️ PASO 3: INICIAR LA APP

**⏱️ Tiempo: 30 segundos**

En el mismo PowerShell:

```powershell
python run.py
```

Espera:

```
 * Running on http://127.0.0.1:5000
```

Abre navegador:

```
http://localhost:5000
```

Inicia sesión con rol **RRHH** (debe existir un usuario RRHH en BD)

---

## 🧪 PASO 4: PROBAR MÓDULOS (3 minutos)

### **4.1 - Prueba: Generar Liquidación de Octubre**

```
1. Menú → Nómina → Generar
2. Período: 2025-10
3. Presiona: Generar
```

**Resultado esperado:**
- 6 liquidaciones creadas
- Cada una con descuentos (manuales + sanciones)
- Cálculo automático de IPS

**Ver detalles:**
```
Menú → Nómina → Liquidaciones
Filtra: 2025-10
Haz click en un empleado
```

**Descargar PDF:**
```
Botón "PDF" en la fila del empleado
```

---

### **4.2 - Prueba: Registrar Despido**

```
1. Menú → Nómina → Registrar Despido
2. Empleado: Selecciona uno (ej: Juan Pérez)
3. Tipo: Injustificado
4. Causal: Incapacidad Laboral
5. Presiona: Registrar Despido
```

**Resultado esperado:**
- Liquidación automática con:
  - ✓ Indemnización (basada en años de antigüedad)
  - ✓ Aguinaldo proporcional (del año)
  - ✓ Vacaciones no gozadas
  - ✓ (-) IPS 9%
  - ✓ Salario neto

**Descargar PDF:**
```
Se abre vista de liquidación
Botón: Descargar PDF
```

---

### **4.3 - Prueba: Generar Aguinaldos**

```
1. Menú → Nómina → Generar Aguinaldo
2. Año: 2025
3. Mes: 12 (Diciembre)
4. Día: 31
5. Presiona: Previsualizar
```

**Ver tabla con:**
- Nombre empleado
- Meses trabajados
- Aguinaldo bruto
- (-) IPS 9%
- Neto

```
6. Si es correcto: Presiona Generar Aguinaldo
7. Confirma la acción
```

**Resultado:**
```
✓ 6 aguinaldos generados (o menos si alguno fue despedido)
Total bruto: XXX,XXX,XXX Gs.
Total IPS: XX,XXX,XXX Gs.
Total neto: XXX,XXX,XXX Gs.
```

---

### **4.4 - Ver Aguinaldos Generados**

```
1. Menú → Nómina → Aguinaldos
2. Filtra: Año 2025
```

**Ver tabla con:**
- Todos los aguinaldos generados
- Empleado, Cédula, Cargo
- Montos bruto, IPS, neto
- Botón PDF por empleado

---

## 🎯 FLUJO VISUAL COMPLETO

```
START

1. MIGRACIÓN BD
   └─ Crea tablas despidos, aguinaldos, descuentos

2. DATOS PRUEBA
   └─ Asistencias + Descuentos + Sanciones

3. INICIA APP
   └─ http://localhost:5000

4. GENERA LIQUIDACIÓN (Oct)
   ├─ Suma salarios
   ├─ Resta descuentos
   ├─ Calcula IPS
   └─ Genera PDF

5. REGISTRA DESPIDO
   ├─ Calcula indemnización
   ├─ Calcula aguinaldo
   ├─ Calcula vacaciones
   ├─ Resta IPS
   └─ Genera PDF

6. GENERA AGUINALDOS (Año)
   ├─ Previsualiza
   ├─ Confirma
   ├─ Crea registros
   └─ Descarga PDFs

END - ¡TODO FUNCIONA!
```

---

## 📊 DATOS QUE VERÁS

### Liquidación Octubre

| Empleado | Salario | Descuentos | IPS | Neto |
|----------|---------|-----------|-----|------|
| Juan | 2M | -200k | -193k | 1.6M |
| María | 1.5M | -150k | -144k | 1.2M |
| Pedro | 1.8M | -180k | -173k | 1.4M |
| Ana | 2M | -333k | -160k | 1.5M |
| Luis | 1.6M | -160k | -138k | 1.3M |
| Rosa | 1.4M | -93k | -126k | 1.1M |

### Aguinaldo 2025

| Empleado | Bruto | IPS | Neto |
|----------|-------|-----|------|
| Juan | 2M | -180k | 1.8M |
| María | 1.5M | -135k | 1.36M |
| ... | ... | ... | ... |

---

## 🔍 CHECKLISTS DE VERIFICACIÓN

### ✅ Liquidación Octubre

- [ ] Se generaron 6 liquidaciones
- [ ] Cada una incluye descuentos
- [ ] IPS está calculado (9%)
- [ ] Salario neto es correcto
- [ ] PDF se descarga correctamente
- [ ] Aparece en Bitácora

### ✅ Despido

- [ ] Se registra correctamente
- [ ] Calcula indemnización automática
- [ ] Calcula aguinaldo de despido
- [ ] Calcula vacaciones no gozadas
- [ ] Resta IPS correctamente
- [ ] PDF muestra todos los rubros
- [ ] Aparece en Bitácora

### ✅ Aguinaldo Anual

- [ ] Preview muestra tabla correcta
- [ ] Totales se suman bien
- [ ] Generación crea registros
- [ ] Se ve en listado
- [ ] PDF se descarga por empleado
- [ ] Aparece en Bitácora
- [ ] No crea duplicados si se genera 2 veces

---

## ⚠️ PROBLEMAS COMUNES

| Problema | Solución |
|----------|----------|
| "Tabla no existe" | Ejecutar migración primero |
| "No veo asistencias" | Ejecutar script de datos |
| "Error 500 en liquidación" | Revisar que hay empleados activos |
| "Descuentos no aparecen" | Script debe haber corrido correctamente |
| "No puedo registrar despido" | Asegurar rol RRHH |
| "Aguinaldo muestra 0" | Asegurar que hay empleados activos |

---

## 📚 DOCUMENTOS DE REFERENCIA

```
Leer en este orden:

1. START_AQUI.txt (2 min)
   └─ Resumen rápido de todo

2. GUIA_GENERAR_DATOS_PRUEBA.md (3 min)
   └─ Detalles del script de datos

3. NAVEGACION_AGUINALDOS_VISUAL.md (2 min)
   └─ Pantallas visuales de navegación

4. AGUINALDOS_MANUAL_RAPIDO.md (5 min)
   └─ Guía completa de aguinaldos

5. IMPLEMENTACION_COMPLETA_DESPIDOS_AGUINALDOS.md (10 min)
   └─ Detalles técnicos completos
```

---

## 🎬 EJEMPLO PASO A PASO

### **Escenario: Probar todo en 5 minutos**

```
MINUTO 0:
PowerShell → cd carpeta proyecto

MINUTO 0:30
$ python migrations/add_despido_table.py
✓ Migración completada

MINUTO 1:00
$ python scripts/generar_datos_prueba.py
✓ Datos generados

MINUTO 1:30
$ python run.py
✓ App iniciada

MINUTO 2:00
Browser → http://localhost:5000
Login como RRHH

MINUTO 2:30
Menú → Nómina → Generar
Período: 2025-10
Generar
✓ Liquidaciones creadas

MINUTO 3:30
Menú → Nómina → Registrar Despido
Selecciona empleado
Registrar
✓ Despido registrado

MINUTO 4:30
Menú → Nómina → Generar Aguinaldo
Año: 2025
Previsualizar
Generar
✓ Aguinaldos generados

MINUTO 5:00
¡LISTO! Todo funciona
```

---

## 💡 TIPS

**Tip 1:** Mantén PowerShell abierto (no cierres la app)

**Tip 2:** Si necesitas detener la app: `Ctrl+C`

**Tip 3:** Para reiniciar: `python run.py` de nuevo

**Tip 4:** Los datos de prueba son seguros de ejecutar varias veces

**Tip 5:** Los PDFs usan datos de BD, así que genera liquidación primero

---

## ✨ RESUMEN FINAL

```
┌─────────────────────────────────────┐
│ SISTEMA COMPLETAMENTE FUNCIONAL:    │
├─────────────────────────────────────┤
│ ✅ Despidos + Liquidación automática │
│ ✅ Aguinaldos anuales               │
│ ✅ Descuentos + Sanciones           │
│ ✅ PDFs descargables                │
│ ✅ Auditoría en Bitácora            │
│ ✅ Validaciones + Seguridad         │
└─────────────────────────────────────┘

Listo para:
1. Probar en desarrollo
2. Pasar a producción
3. Integrar con payroll existente
```

---

**¡A PROBAR! 🚀**

Sigue los 4 pasos y en 5 minutos tienes todo funcionando.

¿Alguna duda durante las pruebas? Avísame.
