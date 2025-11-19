# 👨‍👩‍👧‍👦 Bonificación Familiar - Manual Rápido

## 📋 Base Legal

Según la legislación laboral paraguaya, la bonificación familiar es un beneficio que equivale al **5% del salario mínimo vigente por cada hijo** del trabajador.

## 💰 ¿Cómo se calcula?

```
Bonificación Familiar = (Salario Mínimo × 5%) × Cantidad de hijos activos
```

**Ejemplo (2025):**
- Salario mínimo: Gs. 2.798.309
- 5% = Gs. 139.915 por hijo
- Empleado con 2 hijos = Gs. 279.830 mensuales

## 👶 Tipos de Hijos que califican

### 1. Menor de 18 años
- **Requisito:** Tener menos de 18 años
- **Documento:** Certificado de nacimiento
- **Vigencia:** Hasta cumplir 18 años (baja automática)

### 2. Mayor de 18 años (Estudiante)
- **Requisito:** Tener más de 18 años Y estar estudiando
- **Documentos:** 
  - Certificado de nacimiento
  - Certificado de estudios (actualizado anualmente)
- **Vigencia:** Mientras presente certificados de estudio actualizados

### 3. Con Discapacidad
- **Requisito:** Tener discapacidad certificada (cualquier edad)
- **Documentos:**
  - Certificado de nacimiento
  - Certificado de discapacidad
- **Vigencia:** Permanente (mientras persista la condición)

## 📝 Cómo Registrar Hijos

### Desde Perfil de Empleado

1. Ir a **RRHH** → **Empleados**
2. Click en **Ver** del empleado
3. Click en la pestaña **Hijos**
4. Click en **Agregar Hijo**

### Datos Requeridos

- **Nombre y Apellido** del hijo
- **Cédula de Identidad**
- **Fecha de Nacimiento**
- **Sexo**
- **Tipo de Hijo** (seleccionar según corresponda)

### Subir Documentos

El sistema permite subir **3 tipos de documentos** por hijo:

1. **Certificado de Nacimiento** (obligatorio para todos)
2. **Certificado de Estudios** (obligatorio para estudiantes mayores de 18)
3. **Certificado de Discapacidad** (obligatorio para casos de discapacidad)

**Formatos aceptados:** PDF, JPG, PNG  
**Ubicación:** Los archivos se guardan en `app/uploads/bonificaciones/`

## 🔄 Gestión de Hijos

### Ver Listado

Menú **Nómina** → **Bonificación Familiar** → Seleccionar empleado

El listado muestra:
- Datos del hijo (nombre, CI, edad)
- Tipo de hijo
- Estado (Activo/Inactivo)
- Iconos para ver documentos
- Acciones (editar, dar de baja, reactivar)

### Editar Hijo

Click en botón **Editar** (lápiz azul):
- Actualizar datos
- Reemplazar documentos vencidos
- Cambiar tipo si corresponde

### Dar de Baja

Click en botón **Dar de Baja** (X roja):
- Se solicitará motivo de baja
- El hijo pasa a estado **Inactivo**
- Ya NO se calcula bonificación para ese hijo
- **Nota:** No elimina el registro, solo lo inactiva

### Reactivar

Si se dio de baja por error:
- Click en **Reactivar**
- El hijo vuelve a estado **Activo**
- Se reanuda el cálculo de bonificación

## 💼 Integración con Liquidaciones

### Cálculo Automático

Al generar liquidaciones mensuales, el sistema:

1. **Busca salario mínimo vigente** para la fecha de liquidación
2. **Cuenta hijos activos** del empleado para esa fecha
3. **Calcula bonificación:** `(Salario Mínimo × 5%) × Hijos`
4. **Registra en liquidación** en campo `bonificacion_familiar`
5. **Suma al salario neto** del empleado

### Verificar en Recibo

La bonificación familiar aparece como:
- **Línea independiente** en la sección de ingresos
- **Incluida en total devengado**
- **Sumada al salario neto final**

## 📊 Reportes

### Reporte Consolidado

Menú **Nómina** → **Bonificación Familiar**

Muestra:
- **Total de empleados** con hijos registrados
- **Total de hijos activos** en el sistema
- **Total de bonificación mensual** a pagar
- Detalle por empleado (cantidad hijos + monto)

### Información por Empleado

En perfil del empleado, pestaña **Hijos**:
- Resumen de hijos activos
- Monto de bonificación mensual
- Acceso rápido a gestión completa

## ⚙️ Gestión de Salarios Mínimos

### Registrar Nuevo Salario Mínimo

Menú **Nómina** → **Salarios Mínimos** → **Registrar Nuevo**

**Datos requeridos:**
- **Año:** Año de aplicación (ej: 2025)
- **Monto:** Valor del salario mínimo en Guaraníes
- **Vigencia Desde:** Fecha de inicio de vigencia
- **Vigencia Hasta:** Fecha final (opcional, dejar vacío si es actual)

**Ejemplo:**
```
Año: 2025
Monto: 2.798.309
Vigencia Desde: 2025-01-01
Vigencia Hasta: (vacío - es el actual)
```

### Historial

El listado muestra:
- Todos los salarios mínimos registrados
- Ordenados por año (más reciente primero)
- Badge **VIGENTE** en el actual
- Fechas de vigencia de cada uno

### ¿Por qué registrar histórico?

- Para cálculos retroactivos correctos
- Para liquidaciones de meses pasados
- Para aguinaldos que consideran todo el año
- Para auditoría y trazabilidad

## ✅ Checklist de Implementación

### Para Administradores

- [ ] Registrar salario mínimo vigente 2025
- [ ] Revisar lista de empleados con hijos
- [ ] Solicitar documentos a empleados
- [ ] Registrar hijos de cada empleado
- [ ] Subir documentos escaneados
- [ ] Verificar cálculo en próxima liquidación

### Para RRHH

- [ ] Crear protocolo de solicitud de documentos
- [ ] Establecer calendario de actualización de certificados de estudio
- [ ] Definir proceso de verificación de documentos
- [ ] Configurar recordatorios para renovación de certificados
- [ ] Revisar casos de hijos próximos a cumplir 18 años

## 🔔 Recordatorios Importantes

### Actualización Anual

**Estudiantes mayores de 18 años:**
- Solicitar certificado de estudios actualizado cada año
- Si no presentan certificado, dar de baja
- Registrar en bitácora el motivo

### Cumpleaños 18 años

**Hijos menores de 18:**
- Cuando cumplen 18 años, verificar si estudian
- Si NO estudian: dar de baja
- Si estudian: cambiar tipo a "Mayor Estudiante" + subir certificado

### Cambio de Salario Mínimo

**Cada año:**
- Registrar nuevo salario mínimo cuando se publique decreto
- Establecer fecha de vigencia correcta
- Cerrar vigencia del salario anterior

## 🔐 Seguridad y Privacidad

### Documentos

- Los archivos se guardan con nombre aleatorio seguro
- Solo usuarios con rol RRHH o Admin pueden ver documentos
- Los archivos NO son accesibles públicamente
- Ruta protegida: `app/uploads/bonificaciones/`

### Datos Sensibles

- Cédula de identidad de hijos: uso interno solamente
- Certificados de discapacidad: confidenciales
- Acceso restringido por roles de usuario

## ❓ Preguntas Frecuentes

### ¿Se paga bonificación en aguinaldo?

**NO.** La bonificación familiar es un ingreso **HABITUAL** que:
- Se paga mensualmente en la liquidación
- **SÍ se incluye** en el cálculo del aguinaldo (forma parte del "total devengado")
- Pero NO se paga como bonificación separada en diciembre

### ¿Se paga bonificación en vacaciones?

**SÍ.** Como es parte del salario habitual, se incluye en:
- Liquidación de vacaciones
- Cálculo de indemnizaciones
- Preaviso
- Cualquier cálculo basado en salario

### ¿Qué pasa si el hijo cumple 18 a mitad de mes?

El sistema calcula por mes completo:
- Si está activo el día de la liquidación → se paga
- Dar de baja después del pago de ese mes
- A partir del mes siguiente ya no se paga

### ¿Se puede agregar hijos retroactivamente?

Técnicamente **SÍ**, pero:
- Requiere recalcular liquidaciones pasadas
- Debe tener documentación que justifique la retroactividad
- Consultar con contador antes de proceder
- Registrar en bitácora el motivo

## 📞 Soporte

Para dudas o problemas con el módulo:
1. Verificar que salario mínimo vigente esté registrado
2. Revisar que documentos estén correctamente subidos
3. Verificar estado del hijo (Activo/Inactivo)
4. Consultar bitácora para ver historial de cambios

---

**Última actualización:** Enero 2025  
**Versión del sistema:** RRHH2 con PostgreSQL
