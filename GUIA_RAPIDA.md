# 🚀 Guía Rápida - Nuevas Funcionalidades (Diciembre 2025)

## 📋 Tabla de Contenidos
1. [Sistema de Contratación de Postulantes](#sistema-de-contratación-de-postulantes)
2. [Logo Empresarial](#logo-empresarial)
3. [Configuración Inicial](#configuración-inicial)

---

## 1️⃣ Sistema de Contratación de Postulantes

### ¿Qué es?
Un sistema automatizado que permite **convertir postulantes en empleados** con un solo clic, manteniendo todos los datos y validando duplicados.

### ¿Cómo usar?

#### Paso 1: Ver lista de postulantes
```
Menú → RRHH → Postulantes
```

#### Paso 2: Seleccionar postulante
- Click en **"Ver"** para ver detalles
- O click en **botón verde ✅** para contratación rápida

#### Paso 3: Contratar
1. Click en **"🎉 Contratar como Empleado"**
2. Se abre modal con:
   - ✅ Datos del postulante (nombre, email, teléfono)
   - ⚠️ Campos obligatorios:
     - **CI**: Solo números (ej: 1234567)
     - **Código**: Auto-generado (EMP-001, EMP-002...)
     - **Cargo**: Dropdown con salarios
     - **Salario**: Auto-completado según cargo
     - **Fecha ingreso**: Default hoy
3. Completar CI (obligatorio)
4. Ajustar salario si es necesario
5. **"✅ Confirmar Contratación"**

#### Resultado:
- ✅ Empleado creado
- ✅ Postulante marcado como "Contratado"
- ✅ Vinculación automática entre ambos
- ✅ Redirige a perfil del nuevo empleado
- ✅ Registro en bitácora

### ⚠️ Validaciones Automáticas

#### Email duplicado:
```
"El email ya está registrado. Use uno diferente o déjelo vacío"
```
**Solución**: En el modal, modificar el campo "Email del Empleado" o dejarlo vacío.

#### CI duplicado:
```
"La cédula ya está registrada en el sistema"
```
**Solución**: Verificar si el empleado ya existe o corregir CI.

#### Código duplicado:
```
"El código ya existe. Use otro código"
```
**Solución**: Modificar el código sugerido (ej: EMP-010 → EMP-010A).

### 💡 Tips
- El **código se genera automáticamente** (secuencial)
- El **salario se auto-completa** al seleccionar cargo
- El **email es opcional** (puede dejarse vacío)
- Desde la lista, el **botón verde ✅** abre el modal directamente

---

## 2️⃣ Logo Empresarial

### ¿Qué es?
Sistema que muestra el **logo de tu empresa** en todas las pantallas y documentos PDF.

### ¿Dónde aparece?

#### 🔓 Login (Sin autenticación)
- Logo centrado grande
- Nombre de la empresa
- Branding profesional

#### 📊 Dashboard
- Header con logo
- Datos completos de empresa:
  - RUC
  - Dirección
  - Teléfono y email

#### 🧭 Navbar
- Logo pequeño en todas las páginas
- Junto a "Sistema RRHH"

#### 📄 Reportes PDF
- Membrete oficial con logo
- En recibos de salario
- En planillas mensuales
- En contratos (si implementado)

### ¿Cómo configurar?

#### Paso 1: Ir a configuración
```
Menú → RRHH → Empresa → Configurar
```

#### Paso 2: Subir logo
1. Scroll a "Logo de la Empresa"
2. Click **"Cambiar Logo"**
3. Seleccionar archivo (PNG, JPG, GIF)
4. Click **"Guardar Cambios"**

#### Paso 3: Verificar
1. Logout del sistema
2. Ver pantalla de login → Logo debe aparecer
3. Login nuevamente
4. Dashboard → Header con logo
5. Descargar un recibo PDF → Membrete con logo

### 📏 Especificaciones del Logo

#### Formatos aceptados:
- ✅ PNG (recomendado - con transparencia)
- ✅ JPG / JPEG
- ✅ GIF

#### Tamaños recomendados:
- **Login**: 220px × 120px
- **Navbar**: 120px × 40px
- **Dashboard**: 200px × 80px
- **PDF**: 200px × 100px (2" × 1" a 96 DPI)

#### Peso:
- Recomendado: < 500KB
- Sin límite técnico

#### Tips:
- Usar **PNG transparente** para mejor resultado
- El sistema **mantiene proporciones** automáticamente
- Si es muy grande, se **redimensiona automáticamente**

### 🎨 Fallback (sin logo)

Si NO subes logo, el sistema muestra:
- **Login/Dashboard**: Iniciales en círculo con gradiente
  - Ejemplo: "Cooperativa" → "CO"
- **Navbar**: Iniciales en cuadrado redondeado
- **PDF**: Solo texto (sin logo)

---

## 3️⃣ Configuración Inicial

### Primera vez usando el sistema

#### 1. Configurar Empresa
```
RRHH → Empresa → Configurar
```
Completar:
- ✅ Nombre de la empresa
- ✅ RUC
- ✅ Dirección y ciudad
- ✅ Teléfono y email
- ✅ Número patronal IPS
- ✅ **Subir logo** (importante)

#### 2. Crear Cargos
```
RRHH → Empleados → Cargos
```
Ejemplos:
- Gerente General - ₲ 5.000.000
- Contador - ₲ 3.500.000
- Administrativo - ₲ 2.500.000

#### 3. Agregar Postulantes
```
RRHH → Postulantes → Nuevo
```
Completar datos del candidato.

#### 4. Contratar Postulante
```
RRHH → Postulantes → Ver → Contratar
```
Seguir pasos del modal.

#### 5. Verificar
```
RRHH → Empleados → Listar
```
Verificar que el empleado aparezca.

---

## 🆘 Troubleshooting

### Problema: Logo no aparece

**Posibles causas:**
1. Archivo muy grande
2. Formato no soportado
3. Error al subir

**Solución:**
1. Comprimir imagen (< 500KB)
2. Convertir a PNG
3. Subir nuevamente
4. Refrescar navegador (Ctrl+F5)

### Problema: Email duplicado al contratar

**Solución:**
1. En el modal, modificar el campo "Email del Empleado"
2. O dejarlo vacío
3. Intentar nuevamente

### Problema: Código duplicado

**Solución:**
1. El sistema sugiere el próximo código
2. Si falla, modificar manualmente (EMP-010A)

### Problema: Logo se ve distorsionado

**Solución:**
1. Usar imagen con proporciones adecuadas
2. PNG transparente funciona mejor
3. Tamaño recomendado: 220×120px para login

---

## 📞 Soporte

Para más ayuda:
1. Revisar `README.md`
2. Revisar `CHANGELOG.md`
3. Crear issue en GitHub

---

**Última actualización: Diciembre 2025**
