# Changelog - Sistema RRHH

Todos los cambios importantes del proyecto serán documentados en este archivo.

## [2.1.0] - 2025-12-02

### ✨ Nuevas Funcionalidades

#### Sistema de Contratación de Postulantes
- **Modal inteligente de contratación** con validaciones en tiempo real
- **Auto-generación de código de empleado** secuencial (EMP-001, EMP-002...)
- **Mapeo automático** de datos: postulante → empleado
- **Validación de duplicados**: CI, email, código de empleado
- **Vinculación bidireccional** automática entre postulante y empleado
- **Botón rápido** de contratación desde lista de postulantes
- **Campo email editable** en modal para resolver duplicados
- **Salario auto-completado** al seleccionar cargo
- **Registro en bitácora** de todas las contrataciones

#### Identidad Corporativa - Sistema de Logos
- **Logo empresarial en login** (acceso público sin autenticación)
- **Logo en navbar** de todas las páginas autenticadas
- **Header empresarial en dashboard** con logo y datos completos
- **Membrete profesional en PDFs** (recibos de salario, planillas)
- **Context processor global** para empresa disponible en todos los templates
- **Sistema de fallback elegante**:
  - Iniciales con gradiente si no hay logo
  - Ícono genérico como último recurso
- **Ruta pública** `/rrhh/uploads/empresa/*` para logos
- **Ruta protegida** para otros archivos (requiere autenticación)

### 🔧 Mejoras

#### Backend
- Validación robusta de email duplicado al contratar
- Mejor manejo de errores con mensajes descriptivos
- Optimización de consultas SQL en contratación
- Mejora en generación de códigos de empleado

#### Frontend
- Validaciones JavaScript en tiempo real
- Mejoras en UX del modal de contratación
- Mensajes de error más claros y accionables
- Diseño responsivo mejorado
- Iconos y emojis contextuales

#### Seguridad
- Logos de empresa accesibles públicamente (solo carpeta empresa/)
- Otros archivos mantienen protección de autenticación
- Validación de tipos de archivo en upload de logo

### 🐛 Correcciones
- Fix: Error de email duplicado al contratar postulante
- Fix: Logos no se mostraban en login por @login_required
- Fix: Duplicación de ruta 'empresa/' en URLs de logos
- Fix: Validación de CI solo acepta números

### 📚 Documentación
- README.md actualizado con nuevas funcionalidades
- Scripts de instalación con información de nuevas features
- Changelog creado para trackear cambios
- Comentarios mejorados en código crítico

---

## [2.0.0] - 2025-11-30

### ✨ Funcionalidades Base

#### Core del Sistema
- Gestión completa de empleados, cargos, asistencias
- Sistema de liquidación con anticipos y bonificaciones
- Gestión de permisos, vacaciones y sanciones
- Reportes PDF profesionales
- Bitácora de auditoría completa
- Sistema de autenticación con roles

#### Módulos Implementados
- Gestión de Empleados
- Control de Asistencia con cierre automático (17:30)
- Liquidación de Salarios (Nómina)
- Anticipos con descuento automático
- Bonificación Familiar (5% por hijo)
- Despidos y Finiquitos
- Contratos PDF
- Gestión de Postulantes (sin contratación automática)
- Empresa y Configuración

---

## Formato del Changelog

Este changelog sigue los principios de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y el proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

### Tipos de cambios
- **✨ Nuevas Funcionalidades** - para nuevas características
- **🔧 Mejoras** - para cambios en funcionalidades existentes
- **🐛 Correcciones** - para corrección de bugs
- **🔒 Seguridad** - para correcciones de seguridad
- **📚 Documentación** - para cambios en documentación
- **⚠️ Deprecado** - para funcionalidades que serán removidas
- **🗑️ Removido** - para funcionalidades removidas
