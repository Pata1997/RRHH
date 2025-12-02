# 📘 MANUAL DE USUARIO - SISTEMA RRHH COOPERATIVA

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Gestión de Empleados](#gestión-de-empleados)
4. [Control de Asistencia](#control-de-asistencia)
5. [Gestión de Permisos](#gestión-de-permisos)
6. [Gestión de Vacaciones](#gestión-de-vacaciones)
7. [Gestión de Sanciones](#gestión-de-sanciones)
8. [Liquidaciones de Salario](#liquidaciones-de-salario)
9. [Aguinaldos](#aguinaldos)
10. [Bonificación Familiar](#bonificación-familiar)
11. [Anticipos de Salario](#anticipos-de-salario)
12. [Ingresos Extras](#ingresos-extras)
13. [Planillas Oficiales](#planillas-oficiales)
14. [Despidos](#despidos)
15. [Gestión de Usuarios](#gestión-de-usuarios)
16. [Empresa](#empresa)
17. [Reclutamiento](#reclutamiento)
18. [Bitácora del Sistema](#bitácora-del-sistema)
19. [Casos Especiales y Preguntas Frecuentes](#casos-especiales-y-preguntas-frecuentes)

---

## Introducción

El **Sistema RRHH Cooperativa** es una aplicación web diseñada para gestionar todos los aspectos relacionados con Recursos Humanos de una organización. Permite controlar la asistencia, calcular liquidaciones de salario, gestionar permisos, vacaciones, aguinaldos, y generar planillas oficiales para el MTESS e IPS.

### Características principales:
- ✅ Control de asistencia en tiempo real
- ✅ Cálculo automático de liquidaciones mensuales
- ✅ Gestión de vacaciones y permisos
- ✅ Generación de aguinaldos
- ✅ Bonificación familiar automática
- ✅ Planillas MTESS e IPS
- ✅ Registro de despidos con cálculos de indemnización
- ✅ Formato de montos en Guaraníes (Ej: ₲ 1.000.000)

---

## Acceso al Sistema

### 1.1 Iniciar Sesión

1. Abrir el navegador web (Chrome, Firefox, Edge)
2. Ingresar a la URL del sistema: `http://localhost:5000` o la IP del servidor
3. En la pantalla de login, ingresar:
   - **Usuario**: admin
   - **Contraseña**: admin123

4. Click en **"Iniciar Sesión"**

### 1.2 Usuarios por Defecto

El sistema incluye estos usuarios de prueba:

| Usuario | Contraseña | Descripción |
|---------|-----------|-------------|
| admin | admin123 | Usuario con acceso completo |
| asistente | asistente123 | Usuario asistente de RRHH |

### 1.3 Cambiar Contraseña

1. Click en tu nombre de usuario (esquina superior derecha)
2. Seleccionar **"Cambiar contraseña"**
3. Ingresar:
   - Contraseña actual
   - Nueva contraseña
   - Confirmar nueva contraseña
4. Click en **"Guardar"**

⚠️ **Importante**: La contraseña debe tener al menos 6 caracteres.

### 1.4 Cerrar Sesión

1. Click en tu nombre de usuario (esquina superior derecha)
2. Seleccionar **"Cerrar sesión"**

---

## Gestión de Empleados

### 2.1 Listar Empleados

1. En el menú superior, click en **"Empleados"** → **"Listar"**
2. Verás una tabla con todos los empleados registrados
3. Información visible:
   - Código de empleado
   - Nombre completo
   - CI
   - Cargo
   - Estado (Activo/Inactivo/Suspendido)
   - Fecha de ingreso
   - Acciones disponibles

### 2.2 Crear Nuevo Empleado

1. En el menú superior, click en **"Empleados"** → **"Crear"**
2. Llenar el formulario con los datos del empleado:

#### **Información Personal**
- **Nombre completo**: Nombre y apellido del empleado
- **CI (Cédula de Identidad)**: Sin puntos ni guiones (Ej: 1234567)
- **Fecha de nacimiento**: Usar el selector de fecha
- **Género**: Seleccionar Masculino/Femenino/Otro
- **Estado civil**: Soltero/Casado/Divorciado/Viudo/Unión libre
- **Dirección**: Dirección completa del domicilio
- **Teléfono**: Número de contacto
- **Email**: Correo electrónico

#### **Información Laboral**
- **Cargo**: Seleccionar de la lista desplegable (Ej: Gerente, Asistente, etc.)
- **Fecha de ingreso**: Fecha en que empezó a trabajar
- **Salario base**: Salario mensual en Guaraníes (Ej: 3000000 para ₲ 3.000.000)
- **Estado**: Seleccionar Activo (por defecto para nuevo empleado)

#### **Información Bancaria** (Opcional)
- **Nombre del banco**: Banco donde recibe el salario
- **Número de cuenta**: Número de cuenta bancaria
- **Tipo de cuenta**: Ahorros/Corriente

#### **Información IPS**
- **Número IPS**: Número de afiliación al IPS
- **Fecha de afiliación IPS**: Fecha de inscripción

3. Click en **"Guardar"**
4. El sistema mostrará un mensaje de confirmación

⚠️ **Campos obligatorios**: Nombre completo, CI, cargo, fecha de ingreso, salario base

### 2.3 Editar Empleado

1. En la lista de empleados, click en el botón **"Editar"** (icono de lápiz) del empleado deseado
2. Modificar los campos necesarios
3. Click en **"Guardar cambios"**

💡 **Tip**: Puedes cambiar el salario base aquí cuando haya un aumento.

### 2.4 Cambiar Estado de Empleado

Un empleado puede tener 3 estados:

- **Activo**: Trabaja normalmente, aparece en liquidaciones
- **Inactivo**: No aparece en liquidaciones (usado para despidos o renuncias)
- **Suspendido**: Temporalmente suspendido, no cobra salario

**Para cambiar el estado:**
1. Editar el empleado
2. En el campo **"Estado"**, seleccionar el nuevo estado
3. Guardar cambios

### 2.5 Gestión de Cargos

#### Ver Lista de Cargos
1. En el menú **"Empleados"** → **"Cargos"**
2. Verás todos los cargos disponibles

#### Crear Nuevo Cargo
1. En la pantalla de cargos, click en **"Nuevo Cargo"**
2. Ingresar:
   - **Nombre del cargo**: Ej: "Contador Senior"
   - **Descripción**: Detalle de las funciones (opcional)
3. Click en **"Guardar"**

#### Editar/Eliminar Cargo
- Click en **"Editar"** para modificar
- Click en **"Eliminar"** para borrar (solo si no hay empleados con ese cargo)

### 2.6 Contratos

El sistema registra automáticamente el contrato cuando creas un empleado. Puedes ver y gestionar contratos desde el perfil del empleado.

---

## Control de Asistencia

El sistema de asistencia registra las entradas y salidas de los empleados durante el día laboral.

### 3.1 Horario Laboral Configurado

- **Entrada**: 08:00 AM
- **Salida**: 05:00 PM (17:00)
- **Horario de almuerzo**: 11:30 AM - 1:30 PM (11:30 - 13:30)

### 3.2 Registrar Asistencia

#### Opción A: Registro Manual
1. En el menú superior, click en **"Asistencia"**
2. Buscar al empleado en la lista
3. Click en **"Registrar Entrada"** o **"Registrar Salida"** según corresponda

#### Opción B: Desde el Listado de Empleados
1. En la lista de empleados activos verás su estado actual
2. Click en el botón de acción correspondiente

### 3.3 Tipos de Marcaciones

El sistema detecta automáticamente el tipo de marcación:

1. **Entrada del día**: Primera marcación del día
2. **Salida a almuerzo**: Marcación OUT entre 11:30 y 13:30
3. **Entrada de almuerzo**: Siguiente marcación IN después de salir a almuerzo
4. **Salida del día**: Última marcación OUT del día

### 3.4 Ver Reporte de Asistencia

1. En el menú **"Asistencia"**, click en **"Ver Reporte"**
2. Seleccionar:
   - **Empleado**: Elegir de la lista o "Todos"
   - **Mes**: Seleccionar mes
   - **Año**: Seleccionar año
3. Click en **"Buscar"**

El reporte muestra:
- Fecha
- Hora de entrada
- Hora de salida
- Presente (Sí/No)
- Observaciones detalladas

### 3.5 Observaciones Automáticas

El sistema genera observaciones detalladas (Nivel 2):

- **"Día completo (8h) - Almuerzo 1h"**: Jornada normal completa
- **"Llegada tarde 25 min - Día completo - Almuerzo 1h"**: Llegó tarde pero completó el día
- **"Solo turno mañana - No regresó"**: Solo trabajó la mañana
- **"Solo turno tarde - Ingreso 13:35"**: Solo trabajó la tarde
- **"Salida anticipada 15:45"**: Se retiró antes de las 17:00
- **"Día completo - Sin registro de almuerzo"**: No registró salida/entrada de almuerzo
- **"Vacaciones pagadas"**: Día de vacaciones aprobadas
- **"Permiso con goce de sueldo"**: Permiso aprobado
- **"Ausencia injustificada"**: No asistió sin justificación

### 3.6 Cierre Automático de Asistencia

⚠️ **Importante**: El sistema cierra automáticamente las asistencias a las **17:30** de cada día. Si un empleado no marcó salida, el sistema la registra automáticamente a las 17:00.

### 3.7 Cómo Afecta la Asistencia al Salario

- **Presente = Sí**: El día cuenta completo para el salario (incluye vacaciones, permisos con goce, llegadas tarde)
- **Presente = No**: El día se descuenta del salario

**Fórmula**:
```
Salario ajustado = (Salario base ÷ Días hábiles del mes) × Días presentes
```

💡 **Ejemplo**: 
- Salario base: ₲ 3.000.000
- Días hábiles noviembre: 20
- Días presentes: 18
- Salario ajustado: (3.000.000 ÷ 20) × 18 = ₲ 2.700.000

---

## Gestión de Permisos

### 4.1 Tipos de Permisos

El sistema maneja dos tipos:

1. **Con goce de sueldo**: El empleado cobra ese día normalmente
2. **Sin goce de sueldo**: El día se descuenta del salario

### 4.2 Solicitar Permiso

1. En el menú **"Gestión"** → **"Permisos"**
2. Click en **"Nuevo Permiso"**
3. Llenar el formulario:
   - **Empleado**: Seleccionar de la lista
   - **Fecha inicio**: Primer día del permiso
   - **Fecha fin**: Último día del permiso
   - **Tipo de permiso**: Con goce / Sin goce
   - **Motivo**: Descripción del motivo (Ej: "Trámite médico", "Asunto personal")
   - **Adjuntar documento**: Opcional, subir PDF o imagen justificativa
4. Click en **"Solicitar Permiso"**

El permiso quedará en estado **"Pendiente"** hasta que sea revisado.

### 4.3 Aprobar o Rechazar Permiso

1. En la lista de permisos, buscar los que tienen estado **"Pendiente"**
2. Click en **"Ver Detalle"**
3. Revisar la información
4. Click en:
   - **"Aprobar"**: El permiso se aplicará y afectará la asistencia
   - **"Rechazar"**: Ingresar motivo del rechazo y confirmar

### 4.4 Estados de Permisos

- **Pendiente** ⏳: Esperando aprobación
- **Aprobado** ✅: Permiso otorgado
- **Rechazado** ❌: Permiso denegado

### 4.5 Ver Historial de Permisos

1. En **"Gestión"** → **"Permisos"**
2. Usar los filtros:
   - Por empleado
   - Por estado
   - Por fecha
3. Click en **"Buscar"**

### 4.6 Cómo Afectan los Permisos al Salario

- **Permiso con goce**: Se marca asistencia como **Presente = Sí** → No se descuenta
- **Permiso sin goce**: Se marca asistencia como **Presente = No** → Se descuenta ese día

---

## Gestión de Vacaciones

### 5.1 Días de Vacaciones por Ley

Según la legislación paraguaya:
- Empleados con **menos de 5 años**: **12 días** de vacaciones por año
- Empleados con **5 a 10 años**: **18 días** por año
- Empleados con **más de 10 años**: **30 días** por año

El sistema calcula automáticamente los días disponibles según la antigüedad.

### 5.2 Solicitar Vacaciones

1. En el menú **"Gestión"** → **"Vacaciones"**
2. Click en **"Nueva Solicitud"**
3. Llenar el formulario:
   - **Empleado**: Seleccionar
   - **Fecha inicio**: Primer día de vacaciones
   - **Fecha fin**: Último día de vacaciones
   - **Días solicitados**: Se calcula automáticamente (solo días hábiles)
   - **Observaciones**: Notas adicionales (opcional)
4. Click en **"Solicitar"**

⚠️ **Importante**: El sistema valida que el empleado tenga días disponibles suficientes.

### 5.3 Aprobar Vacaciones

1. En la lista de vacaciones, buscar las **"Pendientes"**
2. Click en **"Ver Detalle"**
3. Verificar:
   - Días solicitados vs. días disponibles
   - Fechas
   - No hay conflictos con otros empleados
4. Click en **"Aprobar"** o **"Rechazar"**

### 5.4 Estados de Vacaciones

- **Pendiente** ⏳: Esperando aprobación
- **Aprobado** ✅: Vacaciones confirmadas
- **Rechazado** ❌: Solicitud denegada
- **Finalizado** 🏁: Vacaciones ya tomadas

### 5.5 Cómo Afectan las Vacaciones al Salario

🎯 **MUY IMPORTANTE**: Las vacaciones son **PAGADAS**.

- Las vacaciones aprobadas se registran en asistencia como **Presente = Sí**
- Observación: **"Vacaciones pagadas"**
- **NO se descuentan del salario**

### 5.6 Ver Días Disponibles

1. En el perfil del empleado, se muestra:
   - Días de vacaciones por año (según antigüedad)
   - Días ya tomados
   - Días disponibles

---

## Gestión de Sanciones

### 6.1 Tipos de Sanciones

El sistema permite registrar sanciones con descuento económico:

- **Llamada de atención**: Sin descuento, solo registro
- **Amonestación**: Con posible descuento
- **Suspensión**: Con descuento de días no trabajados
- **Otra**: Tipo personalizado

### 6.2 Registrar Sanción

1. En el menú **"Gestión"** → **"Sanciones"**
2. Click en **"Nueva Sanción"**
3. Llenar el formulario:
   - **Empleado**: Seleccionar
   - **Tipo de sanción**: Elegir de la lista
   - **Fecha de sanción**: Fecha en que ocurrió
   - **Motivo**: Descripción detallada de la falta
   - **Monto del descuento**: En Guaraníes (0 si no aplica)
   - **Observaciones**: Detalles adicionales (opcional)
   - **Adjuntar documento**: PDF o imagen de acta de sanción (opcional)
4. Click en **"Guardar Sanción"**

### 6.3 Editar Sanción

1. En la lista de sanciones, click en **"Editar"**
2. Modificar los campos necesarios
3. Guardar cambios

### 6.4 Eliminar Sanción

1. Click en **"Eliminar"** en la sanción deseada
2. Confirmar la eliminación

⚠️ **Nota**: Solo se pueden eliminar sanciones antes de generar la liquidación del mes.

### 6.5 Cómo Afectan las Sanciones al Salario

Las sanciones con monto de descuento se aplican en la liquidación mensual:

```
Total Descuentos = Ausencias + Anticipos + Sanciones + Otros
```

En el recibo aparecerá:
- **Descuento por Sanciones**: ₲ [monto]

---

## Liquidaciones de Salario

### 7.1 ¿Qué es una Liquidación?

La liquidación es el cálculo mensual del salario que recibirá cada empleado, considerando:
- Salario base
- Días trabajados
- Ingresos extras
- Bonificación familiar
- Descuentos (ausencias, anticipos, sanciones)
- Aporte IPS (9.625%)

### 7.2 Generar Liquidación Mensual

1. En el menú **"Nómina"** → **"Generar"**
2. Seleccionar:
   - **Mes**: Mes a liquidar
   - **Año**: Año correspondiente
3. El sistema mostrará:
   - Lista de empleados activos
   - Vista previa de los cálculos
4. Verificar los datos
5. Click en **"Generar Liquidaciones"**

⏱️ El proceso puede tardar unos segundos si hay muchos empleados.

### 7.3 Fórmula de Cálculo

```
1. Salario Base del empleado

2. Días hábiles del mes (Ej: noviembre 2025 = 20 días)

3. Contar días presentes (incluye: trabajo normal, vacaciones, permisos con goce, llegadas tarde)

4. Salario ajustado = (Salario base ÷ Días hábiles) × Días presentes

5. Ingresos Extras (si tiene)

6. Bonificación Familiar (si tiene hijos registrados)
   = Número de hijos × (Salario mínimo vigente × 5%)

7. Subtotal Ingresos = Salario ajustado + Ingresos extras + Bonificación familiar

8. Descuentos:
   - Ausencias = Salario base - Salario ajustado
   - Anticipos del mes
   - Sanciones del mes
   - Otros descuentos

9. Total Descuentos = Suma de todos los descuentos

10. Base para IPS = Salario base (NO ajustado)

11. IPS (9.625%) = Base para IPS × 0.09625

12. Total a Descontar = Total Descuentos + IPS

13. SALARIO NETO = Subtotal Ingresos - Total a Descontar
```

### 7.4 Ver Liquidaciones

1. En el menú **"Nómina"** → **"Liquidaciones"**
2. Seleccionar mes y año
3. Click en **"Buscar"**

Se mostrará una tabla con:
- Empleado
- Período
- Salario Base
- Ingresos Extra
- Bonificación Familiar
- Descuentos
- IPS
- **Salario Neto** (en negrita)
- Acciones

### 7.5 Descargar Recibo de Salario (PDF)

1. En la lista de liquidaciones, click en el botón **"PDF"** (icono de documento)
2. El navegador descargará el PDF automáticamente

El recibo incluye:
- Datos del empleado (nombre, CI, código, cargo)
- Período y fecha de emisión
- Desglose completo:
  - Salario Base
  - Ingresos Extras
  - Bonificación Familiar
  - Subtotal Ingresos
  - Descuento por Ausencias
  - Descuento por Anticipos
  - Descuento por Sanciones
  - Otros Descuentos
  - Total Descuentos
  - Aporte IPS (9.625%)
  - Total a Descontar
  - **SALARIO NETO** (destacado)

📄 Formato: Todas las cantidades en formato Guaraníes: **₲ 1.000.000**

### 7.6 Eliminar Liquidación

1. Click en el botón **"Eliminar"** (icono de papelera)
2. Confirmar la eliminación

⚠️ **Cuidado**: Esta acción no se puede deshacer.

### 7.7 Casos Especiales en Liquidaciones

#### Empleado con vacaciones
- Las vacaciones cuentan como días presentes
- NO se descuentan del salario
- En el recibo no aparece descuento por esos días

#### Empleado con permisos con goce
- Igual que vacaciones, cuenta como presente
- No hay descuento

#### Empleado con permisos sin goce
- Se descuenta como ausencia
- Aparece en "Descuento por Ausencias"

#### Empleado con anticipos
- Los anticipos solicitados y aprobados en el mes se descuentan
- Aparece en "Descuento por Anticipos"

#### Empleado que ingresó a mitad de mes
- Solo se calcula proporcional a los días trabajados
- Ejemplo: Ingresó el día 15 de un mes con 20 días hábiles
- Solo cobra: (Salario base ÷ 20) × Días trabajados desde el 15

---

## Aguinaldos

### 8.1 ¿Qué es el Aguinaldo?

Es un salario adicional que se paga una vez al año, equivalente a **1/12 del total de salarios** percibidos en el año (o la proporción si trabajó menos de un año).

Por ley paraguaya se paga en **diciembre**.

### 8.2 Generar Aguinaldos

1. En el menú **"Nómina"** → **"Generar Aguinaldo"**
2. Seleccionar:
   - **Año**: Año del aguinaldo (Ej: 2025)
   - **Mes de pago**: Usualmente diciembre
3. El sistema mostrará:
   - Lista de empleados activos
   - Cálculo automático por empleado
4. Revisar los montos
5. Click en **"Generar Aguinaldos"**

### 8.3 Fórmula de Cálculo del Aguinaldo

```
Aguinaldo = Suma de todos los salarios pagados en el año ÷ 12
```

**Ejemplo**:
- Empleado trabajó todo el año 2025
- Salario mensual: ₲ 3.000.000
- Total pagado en el año: 3.000.000 × 12 = ₲ 36.000.000
- Aguinaldo: 36.000.000 ÷ 12 = **₲ 3.000.000**

**Ejemplo proporcional**:
- Empleado ingresó en julio 2025 (trabajó 6 meses)
- Salario mensual: ₲ 3.000.000
- Total pagado: 3.000.000 × 6 = ₲ 18.000.000
- Aguinaldo: 18.000.000 ÷ 12 = **₲ 1.500.000**

### 8.4 Ver Historial de Aguinaldos

1. En el menú **"Nómina"** → **"Aguinaldos"**
2. Filtrar por año
3. Verás la lista con:
   - Empleado
   - Año
   - Monto del aguinaldo
   - Fecha de pago
   - Estado

### 8.5 Descargar Comprobante de Aguinaldo

1. Click en el botón **"PDF"** del aguinaldo deseado
2. Se descarga el comprobante con:
   - Datos del empleado
   - Año correspondiente
   - Monto del aguinaldo
   - Fecha de pago

---

## Bonificación Familiar

### 9.1 ¿Qué es la Bonificación Familiar?

Es un beneficio obligatorio en Paraguay que consiste en pagar al empleado el **5% del salario mínimo vigente** por cada hijo menor de 18 años (o hasta 25 años si estudia).

### 9.2 Cálculo Automático

El sistema calcula automáticamente:
```
Bonificación Familiar = Número de hijos × (Salario mínimo vigente × 5%)
```

**Ejemplo** (con salario mínimo 2025 de ₲ 2.680.373):
- Empleado con 2 hijos
- Bonificación: 2 × (2.680.373 × 0.05) = 2 × 134.019 = **₲ 268.038**

### 9.3 Registrar Hijos del Empleado

1. Ir a **"Empleados"** → Editar empleado
2. En la sección **"Bonificación Familiar"**, click en **"Agregar Hijo"**
3. Llenar:
   - **Nombre completo del hijo**
   - **Fecha de nacimiento**
   - **CI** (si tiene)
   - **¿Estudia?**: Sí/No (si es mayor de 18)
4. Guardar

El sistema valida:
- Si el hijo es menor de 18 años: cuenta automáticamente
- Si tiene 18-25 años: solo cuenta si estudia
- Si es mayor de 25 años: no cuenta

### 9.4 Ver Reporte de Bonificaciones

1. En el menú **"Nómina"** → **"Bonificación Familiar"**
2. Verás una tabla con:
   - Empleado
   - Número de hijos que califican
   - Monto de bonificación mensual
   - Estado

### 9.5 Gestionar Salarios Mínimos

El sistema necesita tener registrado el salario mínimo vigente para calcular la bonificación.

1. En el menú **"Nómina"** → **"Salarios Mínimos"**
2. Click en **"Nuevo Salario Mínimo"**
3. Ingresar:
   - **Monto**: Salario mínimo oficial (Ej: ₲ 2.680.373)
   - **Fecha de vigencia**: Fecha desde la cual aplica
4. Guardar

💡 **Tip**: Actualizar cada vez que el gobierno decrete nuevo salario mínimo.

---

## Anticipos de Salario

### 10.1 ¿Qué es un Anticipo?

Es un adelanto del salario que se le otorga al empleado durante el mes. Se descuenta en la liquidación mensual.

### 10.2 Solicitar Anticipo

1. En el menú **"Nómina"** → **"Anticipos"** (o desde el perfil del empleado)
2. Click en **"Nuevo Anticipo"**
3. Llenar:
   - **Empleado**: Seleccionar
   - **Monto solicitado**: En Guaraníes
   - **Motivo**: Razón del anticipo
   - **Fecha de solicitud**: Fecha actual (auto-completado)
4. Click en **"Solicitar"**

El anticipo queda en estado **"Pendiente"**.

### 10.3 Aprobar o Rechazar Anticipo

1. En la lista de anticipos, buscar los **"Pendientes"**
2. Click en **"Ver Detalle"**
3. Verificar:
   - Monto solicitado vs. salario del empleado
   - Historial de anticipos previos
4. Click en:
   - **"Aprobar"**: El anticipo se descuenta en la liquidación del mes
   - **"Rechazar"**: Ingresar motivo del rechazo

### 10.4 Estados de Anticipos

- **Pendiente** ⏳: Esperando aprobación
- **Aprobado** ✅: Anticipo otorgado, se descontará
- **Rechazado** ❌: Solicitud denegada
- **Descontado** 💰: Ya fue descontado en la liquidación

### 10.5 Cómo Afectan al Salario

Los anticipos aprobados se descuentan en la liquidación:

```
Descuento por Anticipos = Suma de anticipos aprobados en el mes
```

En el recibo aparece:
- **Descuento por Anticipos**: ₲ [monto]

⚠️ **Límite recomendado**: No exceder el 50% del salario mensual.

---

## Ingresos Extras

### 11.1 ¿Qué son los Ingresos Extras?

Son pagos adicionales al salario base que puede recibir un empleado:
- Horas extras
- Bonos por desempeño
- Comisiones
- Viáticos
- Otros

### 11.2 Registrar Ingreso Extra

1. En el menú **"Nómina"** → **"Ingresos extras"**
2. Click en **"Nuevo Ingreso"**
3. Llenar:
   - **Empleado**: Seleccionar
   - **Tipo**: Horas extras / Bono / Comisión / Viático / Otro
   - **Descripción**: Detalle del ingreso
   - **Monto**: En Guaraníes
   - **Mes**: Mes en que se pagará
   - **Año**: Año correspondiente
4. Click en **"Guardar"**

### 11.3 Ver Ingresos Extras

1. En **"Nómina"** → **"Ingresos extras"**
2. Filtrar por:
   - Empleado
   - Mes
   - Tipo
3. Ver lista con todos los ingresos registrados

### 11.4 Editar/Eliminar Ingreso Extra

- Click en **"Editar"** para modificar
- Click en **"Eliminar"** para borrar

⚠️ Solo se puede editar/eliminar antes de generar la liquidación.

### 11.5 Cómo Afectan al Salario

Los ingresos extras se suman en la liquidación:

```
Subtotal Ingresos = Salario ajustado + Ingresos extras + Bonificación familiar
```

En el recibo aparece:
- **Ingresos Extras**: ₲ [monto]

---

## Planillas Oficiales

### 12.1 Planilla MTESS

Es el reporte oficial que se presenta al **Ministerio de Trabajo, Empleo y Seguridad Social**.

#### Generar Planilla MTESS
1. En el menú **"Planillas"** → **"MTESS"**
2. Seleccionar:
   - **Mes**
   - **Año**
3. Click en **"Generar"**

El sistema muestra una tabla con:
- Nombre completo del empleado
- CI
- Cargo
- Fecha de ingreso
- Salario base
- Total devengado (salario + extras + bonificación)

#### Exportar a Excel
1. Click en **"Exportar a Excel"**
2. Se descarga un archivo `.xlsx` listo para presentar

### 12.2 Planilla IPS / REI

Es el reporte para el **Instituto de Previsión Social** (IPS) y el **Registro de Empleadores** (REI).

#### Generar Planilla IPS
1. En el menú **"Planillas"** → **"IPS / REI"**
2. Seleccionar mes y año
3. Click en **"Generar"**

Muestra:
- Empleado
- CI
- Número IPS
- Salario imponible
- Aporte del empleado (9.625%)
- Aporte del empleador (16.5%)
- Total aportes

#### Exportar
1. Click en **"Exportar a Excel"**
2. Usar el archivo para la declaración en el portal de IPS

### 12.3 Información Importante

📌 **Aporte IPS Empleado**: 9.625% del salario base
📌 **Aporte IPS Empleador**: 16.5% del salario base
📌 **Total**: 26.125% del salario base

El sistema calcula automáticamente todos los aportes.

---

## Despidos

### 13.1 Registrar Despido

1. En el menú **"Nómina"** → **"Registrar Despido"**
2. Llenar el formulario:
   - **Empleado**: Seleccionar
   - **Fecha de despido**: Fecha efectiva del despido
   - **Tipo de despido**:
     - **Justificado**: Con causa legal, sin indemnización
     - **Injustificado**: Sin causa, con indemnización
   - **Motivo**: Descripción detallada
   - **Preaviso**: Sí/No (si se dio preaviso de 30 días)
3. Click en **"Calcular Liquidación"**

### 13.2 Cálculo de Indemnización

El sistema calcula automáticamente según la ley paraguaya:

#### Despido Injustificado
```
Indemnización = Antigüedad × Salario mensual
```

**Ejemplo**:
- Empleado con 3 años de antigüedad
- Salario: ₲ 3.000.000
- Indemnización: 3 × 3.000.000 = **₲ 9.000.000**

#### Preaviso
Si no se dio preaviso de 30 días:
```
Indemnización por preaviso = 50% del salario mensual
```

#### Vacaciones Proporcionales
```
Vacaciones no gozadas = (Días de vacaciones anuales ÷ 12) × Meses trabajados en el año
Monto = (Salario mensual ÷ 30) × Días de vacaciones pendientes
```

#### Aguinaldo Proporcional
```
Aguinaldo = Total ganado en el año ÷ 12
```

### 13.3 Ver Liquidación Final

Después de calcular, el sistema muestra:
- Salario del mes trabajado (proporcional)
- Aguinaldo proporcional
- Vacaciones no gozadas
- Indemnización por despido
- Indemnización por falta de preaviso
- **TOTAL A PAGAR**

### 13.4 Descargar Liquidación de Despido

1. Click en **"Generar PDF"**
2. Se descarga la liquidación final completa

### 13.5 Consecuencias del Despido

Automáticamente:
- El empleado pasa a estado **"Inactivo"**
- Ya no aparece en futuras liquidaciones
- Se registra en la bitácora del sistema

---

## Gestión de Usuarios

### 14.1 Ver Lista de Usuarios

1. En el menú **"Usuarios"**
2. Verás todos los usuarios del sistema con:
   - Nombre de usuario
   - Nombre completo
   - Email
   - Rol
   - Estado (Activo/Inactivo)
   - Fecha de creación
   - Último acceso

### 14.2 Crear Nuevo Usuario

1. Click en **"Nuevo Usuario"**
2. Llenar el formulario:
   - **Nombre de usuario**: Para el login (único)
   - **Email**: Correo electrónico (único)
   - **Nombre completo**: Nombre y apellido
   - **Contraseña**: Mínimo 6 caracteres
   - **Confirmar contraseña**: Debe coincidir
   - **Rol**: Seleccionar
   - **Estado**: Activo (marcado por defecto)
3. Click en **"Crear Usuario"**

### 14.3 Editar Usuario

1. En la lista, click en **"Editar"** del usuario deseado
2. Modificar los campos necesarios
3. Para cambiar contraseña:
   - Ingresar nueva contraseña
   - Confirmar nueva contraseña
   - Si se deja vacío, la contraseña no cambia
4. Guardar cambios

### 14.4 Activar/Desactivar Usuario

1. Click en el botón de **estado** del usuario
2. Confirmar la acción

🔒 **Usuario Inactivo**: No puede iniciar sesión en el sistema

### 14.5 Eliminar Usuario

1. Click en **"Eliminar"**
2. Confirmar en el modal

⚠️ **Restricciones**:
- No puedes eliminar tu propio usuario
- No se puede eliminar si es el último administrador

---

## Empresa

### 15.1 Ver Datos de la Empresa

1. En el menú superior, click en **"Empresa"**
2. Verás todos los datos registrados:
   - Razón social
   - RUC
   - Dirección
   - Teléfono
   - Email
   - Sitio web
   - Número patronal (IPS)
   - Logo (si está cargado)

### 15.2 Editar Datos de la Empresa

1. Click en **"Editar"**
2. Modificar los campos necesarios
3. Para cambiar el logo:
   - Click en **"Seleccionar archivo"**
   - Elegir imagen (PNG, JPG, max 2MB)
4. Click en **"Guardar Cambios"**

💡 **Tip**: Los datos de la empresa aparecen en todos los PDFs generados (recibos, planillas, etc.)

---

## Reclutamiento

### 16.1 Gestión de Postulantes

El sistema permite gestionar candidatos para futuras contrataciones.

#### Ver Lista de Postulantes
1. En el menú **"Reclutamiento"** → **"Postulantes"**
2. Verás la lista con:
   - Nombre
   - CI
   - Email
   - Teléfono
   - Cargo al que postula
   - Estado
   - Fecha de postulación

#### Registrar Nuevo Postulante
1. Click en **"Nuevo Postulante"**
2. Llenar el formulario:
   - **Nombre completo**
   - **CI**
   - **Fecha de nacimiento**
   - **Email**
   - **Teléfono**
   - **Dirección**
   - **Cargo de interés**: Cargo al que postula
   - **CV**: Adjuntar PDF del currículum
   - **Observaciones**: Notas adicionales
3. Click en **"Guardar"**

#### Estados de Postulantes
- **Pendiente**: Recién registrado
- **En Revisión**: Siendo evaluado
- **Preseleccionado**: Pasó primera etapa
- **Seleccionado**: Elegido para contratación
- **Rechazado**: No cumple requisitos
- **Contratado**: Ya fue convertido a empleado

#### Convertir Postulante en Empleado
1. Cuando un postulante es seleccionado
2. Click en **"Contratar"**
3. Se abre el formulario de nuevo empleado con los datos del postulante ya completados
4. Completar datos faltantes (salario, fecha de ingreso, etc.)
5. Guardar

El postulante cambia automáticamente a estado **"Contratado"**.

---

## Bitácora del Sistema

### 17.1 ¿Qué es la Bitácora?

La bitácora registra automáticamente **todas las acciones** realizadas en el sistema para auditoría y trazabilidad.

### 17.2 Ver Bitácora

1. En el menú **"Bitácora"**
2. Verás una tabla con:
   - **Usuario**: Quién realizó la acción
   - **Tabla**: En qué módulo (empleados, liquidaciones, etc.)
   - **Acción**: Tipo de operación (CREATE, UPDATE, DELETE, VIEW)
   - **Detalle**: Descripción de lo realizado
   - **Fecha y Hora**: Timestamp exacto
   - **IP**: Dirección IP desde donde se realizó

### 17.3 Filtrar Bitácora

Usar los filtros disponibles:
- **Por usuario**: Ver acciones de un usuario específico
- **Por tabla/módulo**: Filtrar por empleados, liquidaciones, etc.
- **Por acción**: Solo creaciones, actualizaciones, etc.
- **Por fecha**: Rango de fechas

### 17.4 Acciones Registradas

El sistema registra:
- ✅ Creación de empleados
- ✅ Edición de datos
- ✅ Cambios de salario
- ✅ Generación de liquidaciones
- ✅ Aprobación/rechazo de permisos
- ✅ Aprobación de vacaciones
- ✅ Registro de sanciones
- ✅ Eliminación de registros
- ✅ Inicio de sesión
- ✅ Y mucho más...

💡 **Tip**: Útil para auditorías, resolución de conflictos y cumplimiento normativo.

---

## Casos Especiales y Preguntas Frecuentes

### 18.1 Casos de Asistencia

#### ❓ ¿Qué pasa si un empleado olvida marcar salida?
- El sistema cierra automáticamente a las 17:30 y registra salida a las 17:00
- Se marca el día como completo si entró normalmente

#### ❓ ¿Se descuenta por llegar tarde?
- **NO** se descuenta automáticamente
- Solo se registra en las observaciones: "Llegada tarde X minutos"
- La empresa decide si aplica sanción manual

#### ❓ ¿Un empleado puede marcar desde su celular?
- Actualmente el sistema es web, accesible desde cualquier dispositivo
- Se registra la IP desde donde marca

#### ❓ ¿Cómo registro un permiso de medio día?
- Registrar permiso por el día completo
- El sistema ya detecta automáticamente si solo trabajó medio día en la asistencia
- La observación dirá: "Solo turno mañana" o "Solo turno tarde"

### 18.2 Casos de Liquidaciones

#### ❓ ¿Puedo regenerar una liquidación ya creada?
- Sí, primero elimina la liquidación existente
- Luego genera nuevamente con los datos actualizados

#### ❓ ¿Cómo corrijo un error en una liquidación?
1. Eliminar la liquidación del mes
2. Corregir los datos (asistencia, anticipos, sanciones, etc.)
3. Regenerar la liquidación

#### ❓ ¿Qué pasa si genero liquidación antes de fin de mes?
- Se calcula con los días trabajados hasta ese momento
- Puedes eliminarla y regenerarla a fin de mes con todos los días

#### ❓ ¿El IPS se calcula sobre el salario neto o bruto?
- Se calcula sobre el **salario base** (bruto)
- **NO** sobre el salario ajustado después de descuentos

### 18.3 Casos de Vacaciones

#### ❓ ¿Las vacaciones se descuentan del salario?
- **NO**, las vacaciones son pagadas
- Se marcan como Presente = Sí en la asistencia

#### ❓ ¿Cómo se calculan los días de vacaciones?
- Solo se cuentan **días hábiles** (lunes a viernes)
- Los fines de semana no cuentan

#### ❓ ¿Los días de vacaciones vencen?
- Según la ley paraguaya, deben tomarse dentro del año siguiente
- El sistema no vence automáticamente, gestionar manualmente

#### ❓ ¿Puedo aprobar vacaciones que excedan los días disponibles?
- El sistema validará y mostrará una advertencia
- No permitirá aprobar si excede días disponibles

### 18.4 Casos de Permisos

#### ❓ ¿Diferencia entre permiso con goce y sin goce?
- **Con goce**: Se paga el día, no se descuenta
- **Sin goce**: NO se paga, se descuenta del salario

#### ❓ ¿Cuántos días de permiso con goce puedo dar?
- Depende de la política de la empresa
- El sistema no tiene límite, queda a criterio del aprobador

### 18.5 Casos de Anticipos

#### ❓ ¿Cuál es el monto máximo de anticipo?
- El sistema no tiene límite automático
- Recomendación: No exceder 50% del salario mensual

#### ❓ ¿Puedo dar varios anticipos en el mismo mes?
- Sí, todos se suman y descuentan en la liquidación
- Verificar que el total no exceda el salario

#### ❓ ¿Qué pasa si el anticipo es mayor que el salario neto?
- El sistema generará una liquidación con saldo negativo
- **Atención**: Revisar manualmente estos casos

### 18.6 Casos de Aguinaldos

#### ❓ ¿Empleado que ingresó en medio de año cobra aguinaldo completo?
- No, cobra proporcional a los meses trabajados
- Fórmula: (Total ganado en el año) ÷ 12

#### ❓ ¿Empleado despedido cobra aguinaldo?
- Sí, cobra el aguinaldo proporcional hasta la fecha de despido
- Se incluye en la liquidación final

#### ❓ ¿Debo generar aguinaldo manualmente cada año?
- Sí, el sistema no lo genera automáticamente
- Generarlo en diciembre de cada año

### 18.7 Casos de Bonificación Familiar

#### ❓ ¿El hijo cumplió 18 años, sigue cobrando?
- Solo si está estudiando (hasta 25 años)
- Actualizar el registro del hijo marcando "¿Estudia? = Sí"

#### ❓ ¿El salario mínimo cambió, debo actualizar algo?
- Sí, registrar el nuevo salario mínimo en el sistema
- El cálculo de bonificación se actualizará automáticamente

### 18.8 Problemas Técnicos

#### ❓ No puedo iniciar sesión
- Verificar usuario y contraseña
- Verificar que el usuario esté **Activo**
- Contactar al administrador

#### ❓ El sistema dice "Error al generar liquidación"
- Verificar que todos los empleados tengan salario base
- Verificar que haya registros de asistencia del mes
- Verificar que el salario mínimo esté registrado (para bonificación familiar)

#### ❓ Los PDFs no se descargan
- Verificar que el navegador no esté bloqueando descargas
- Probar con otro navegador (Chrome recomendado)
- Verificar permisos de escritura en carpeta de descargas

#### ❓ Los montos no tienen formato Guaraníes
- Verificar que el filtro `|gs` esté aplicado en las plantillas
- Reportar al administrador del sistema

---

## 📞 Soporte

Si tienes problemas o dudas adicionales:

1. **Revisar este manual** completo
2. **Consultar la Bitácora** para ver historial de acciones
3. **Contactar al administrador del sistema**

---

## 📝 Notas Finales

### Mejores Prácticas

✅ **Respaldar la base de datos regularmente**
✅ **Generar liquidaciones al finalizar cada mes**
✅ **Revisar asistencias diariamente**
✅ **Mantener actualizados los datos de empleados**
✅ **Verificar permisos y vacaciones antes de aprobar**
✅ **Descargar PDFs de liquidaciones antes de eliminar**
✅ **Revisar la bitácora periódicamente**
✅ **Actualizar salario mínimo cuando cambie**

### Recomendaciones de Seguridad

🔒 **Cambiar contraseñas por defecto**
🔒 **No compartir credenciales**
🔒 **Cerrar sesión al terminar**
🔒 **Usar contraseñas seguras (8+ caracteres, letras, números, símbolos)**
🔒 **Revisar accesos en la bitácora**

---

**Versión del Manual**: 1.0
**Fecha**: Noviembre 2025
**Sistema**: RRHH Cooperativa v2.0

---

*Este manual cubre todas las funcionalidades del sistema. Para casos no contemplados o dudas específicas, consultar con el administrador del sistema.*
