# Sistema de Gestión de Recursos Humanos (RRHH) - Cooperativa

Una aplicación web completa para la gestión de recursos humanos desarrollada con **Flask**, **PostgreSQL** y **Bootstrap 5**.

## 🚀 Características Principales

### 1. **Gestión de Empleados**
- Registro, edición y eliminación de empleados
- Información personal y laboral completa
- Estados de empleado (Activo, Inactivo, Suspendido, Jubilado)
- Búsqueda y filtrado de empleados
- **Perfil detallado con métricas de asistencias y justificaciones** 🆕

### 2. **Gestión de Cargos**
- CRUD de cargos
- Salario base configurable por cargo
- Descripción de funciones

### 3. **Control de Asistencia**
- Registro de entrada/salida por código de empleado
- Interfaz simple para escaneo rápido
- Bitácora completa de asistencias
- Edición manual de registros
- **Cierre automático a las 17:30** 🆕
- **Justificaciones con estados (Pendiente/Justificado/Injustificado)** 🆕
- **API de métricas de asistencias por empleado** 🆕

### 4. **Gestión de Permisos**
- Solicitud de permisos (enfermedad, asunto personal, etc.)
- Aprobación/rechazo de solicitudes
- Cálculo automático de días
- Historial de permisos

### 5. **Sanciones Disciplinarias**
- Registro de sanciones (amonestación, descuento, suspensión)
- Monto configurable
- Descripción y motivos
- **Integración automática con descuentos en liquidación** ✅

### 6. **Liquidación de Salarios (Nómina)** 💰
- Generación automática de liquidaciones mensuales
- Cálculo de:
  - Salario base proporcional a días trabajados
  - Ingresos extras (bonos + horas extra)
  - **Anticipos con descuento automático** 🆕
  - Bonificación familiar (5% × hijos)
  - Descuentos manuales y sanciones
  - Aporte IPS (9.625%)
  - Salario neto
- **Validación de días hábiles vs días presentes** 🆕
- **Logging detallado de cada componente** 🆕
- **Marcado automático de anticipos como aplicados** 🆕
- Generación de recibos en PDF
- Planilla consolidada mensual
- **API de pre-visualización de liquidación** 🆕

### 7. **Gestión de Anticipos** 🆕
- Solicitud de anticipos con archivo PDF adjunto
- Aprobación/rechazo de solicitudes
- Validación: máximo 40% del salario base
- **Descuento automático en liquidación del mes** ✅
- Marcado como "aplicado" tras liquidar
- **API de anticipos pendientes** 🆕
- **Auditoría de anticipos no descontados** 🆕

### 8. **Gestión de Vacaciones**
- Solicitud de vacaciones
- Seguimiento de días disponibles, tomados y pendientes
- Aprobación de solicitudes

### 9. **Bonificación Familiar** 👨‍👩‍👧
- Registro de hijos/dependientes
- Cálculo automático del 5% por hijo
- Integración en liquidación mensual
- Historial de bonificaciones

### 10. **Despidos y Finiquitos**
- Registro de despidos con causa
- Cálculo de indemnización según legislación
- Gestión de finiquitos
- Estados: Procesando/Pagado/Impugnado

### 11. **Contratos**
- Generación de contratos en PDF con ReportLab
- Información del empleado y condiciones
- Renovación automática de contratos temporales

### 12. **Reportes y PDFs**
- Recibo individual de salario
- Planilla de liquidación mensual
- Contrato de trabajo
- **Auditoría de anticipos (SQL + Python)** 🆕

### 13. **Bitácora de Auditoría**
- Registro de todas las acciones CRUD
- Información del usuario, fecha, hora y detalles
- Filtrado por usuario y módulo
- Trazabilidad completa del sistema

### 14. **Autenticación y Autorización**
- Sistema de login seguro
- Dos roles: RRHH y Asistente RRHH
- Control de acceso por roles
- Cambio de contraseña

### 15. **Gestión de Postulantes** 🆕 👥
- Registro de candidatos con datos personales y laborales
- Estados: Nuevo, En Evaluación, Contratado, Rechazado, En Espera
- Adjunto de documentos (CV, certificados)
- **Sistema de contratación inteligente** ✨
  - Modal interactivo con validaciones en tiempo real
  - Auto-generación de código de empleado secuencial
  - Mapeo automático de datos postulante → empleado
  - Validación de CI, email y código duplicados
  - Vinculación automática postulante-empleado
  - Salario auto-completado según cargo
- Botón rápido de contratación desde lista
- Historial completo de documentos adjuntos

### 16. **Identidad Corporativa** 🆕 🏢
- **Logo empresarial en todo el sistema**
  - Login con logo centrado y branding profesional
  - Navbar con logo integrado en todas las páginas
  - Dashboard con header empresarial completo (logo + datos)
  - Reportes PDF con membrete oficial y logo
- **Sistema de fallback elegante**
  - Iniciales con gradiente si no hay logo
  - Iconos Bootstrap como último recurso
- **Logos públicos en login** (sin autenticación)
- Context processor global para empresa en todos los templates

### 17. **Interfaz Moderna**
- Bootstrap 5 responsivo
- DataTables para tablas interactivas
- SweetAlert2 para confirmaciones
- Alertas flash para retroalimentación
- Navbar con menús dinámicos
- **Perfil de empleado con tabs y estadísticas** 🆕
- Modales interactivos con validaciones JavaScript

### 18. **APIs REST** 🆕
- `/rrhh/liquidaciones/preview/<periodo>` - Pre-visualización de liquidación
- `/rrhh/anticipos/pendientes` - Anticipos sin aplicar
- `/rrhh/metricas/asistencias` - Estadísticas de asistencias
- `/rrhh/api/empleados/<id>/justificaciones` - Historial de justificaciones
- `/rrhh/postulantes/<id>/contratar` - Contratar postulante como empleado 🆕
- `/rrhh/uploads/<path>` - Servir archivos (logos públicos, documentos privados)

## 📁 Estructura del Proyecto

```
RRHH2/
├── app/
│   ├── __init__.py              # Factory de la aplicación
│   ├── config.py                 # Configuraciones
│   ├── models.py                 # Modelos de base de datos
│   ├── bitacora.py               # Funciones de auditoría
│   ├── routes/
│   │   ├── auth.py               # Autenticación
│   │   ├── rrhh.py               # Rutas principales
│   │   └── main.py               # Dashboard y inicio
│   ├── reports/
│   │   └── report_utils.py       # Generación de PDFs
│   ├── templates/
│   │   ├── base.html             # Plantilla base
│   │   ├── dashboard.html        # Dashboard
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── cambiar_password.html
│   │   └── rrhh/
│   │       ├── empleados.html
│   │       ├── asistencia.html
│   │       ├── permisos.html
│   │       ├── liquidaciones.html
│   │       └── más...
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── rrhh.js
├── run.py                        # Punto de entrada
├── requirements.txt              # Dependencias
├── .env                          # Variables de entorno
└── README.md                     # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask 2.3.3
- **Base de Datos**: PostgreSQL 14+
- **ORM**: SQLAlchemy 3.0.5
- **Autenticación**: Flask-Login 0.6.2
- **Reportes**: ReportLab 4.0.7
- **Scheduler**: Flask-APScheduler 1.13.1 (cierre automático de asistencias)
- **Frontend**: Bootstrap 5, DataTables, SweetAlert2, Chart.js
- **Python**: 3.8+

## 📦 Dependencias

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
Flask-APScheduler==1.13.1
Werkzeug==2.3.7
psycopg2-binary==2.9.7
reportlab==4.0.7
python-dotenv==1.0.0
WTForms==3.0.1
email-validator==2.0.0
Jinja2==3.1.2
openpyxl==3.1.2
```

## ⚙️ Instalación

### Requisitos Previos
- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd RRHH2
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env`:
   ```
   FLASK_ENV=development
   SECRET_KEY=tu-clave-secreta-super-segura-min-32-caracteres
   DATABASE_URL=postgresql://rrhh_user:password@localhost/rrhh_db
   ```

5. **Crear base de datos en PostgreSQL**
   ```sql
   CREATE DATABASE rrhh_db;
   CREATE USER rrhh_user WITH PASSWORD 'tu_password';
   ALTER ROLE rrhh_user SET client_encoding TO 'utf8';
   ALTER ROLE rrhh_user SET default_transaction_isolation TO 'read committed';
   GRANT ALL PRIVILEGES ON DATABASE rrhh_db TO rrhh_user;
   ```

6. **Inicializar base de datos**
   ```bash
   python run.py
   flask init-db
   ```

7. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

8. **Acceder a la aplicación**
   
   Abrir navegador en `http://localhost:5000`

## 👤 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | RRHH |
| asistente | asistente123 | Asistente RRHH |

## 🔐 Seguridad

- Contraseñas hasheadas con Werkzeug
- CSRF protection
- SQL Injection prevention con SQLAlchemy
- Session cookies seguras
- Roles y permisos implementados
- Bitácora de auditoría de todas las acciones

## 📊 Base de Datos

### Tablas Principales
- **usuarios**: Credenciales y roles
- **empleados**: Información del empleado
- **cargos**: Cargos disponibles
- **asistencias**: Registro de asistencia con justificaciones 🆕
- **permisos**: Solicitudes de permisos
- **sanciones**: Disciplina (auto-genera descuentos)
- **descuentos**: Descuentos manuales y automáticos
- **anticipos**: Solicitudes de anticipos con aprobación 🆕
- **ingresos_extra**: Bonos adicionales
- **horas_extra**: Horas extra trabajadas
- **bonificacion_familiar**: Hijos/dependientes para bonificación 🆕
- **liquidaciones**: Nómina mensual (incluye anticipos) 🆕
- **vacaciones**: Gestión de vacaciones
- **contratos**: Contratos de trabajo
- **despidos**: Registro de despidos y finiquitos 🆕
- **bitacora**: Auditoría de acciones

## 📈 Reportes Disponibles

1. **Recibo Individual de Salario** (PDF)
   - Detalles personales y laborales
   - Desglose de ingresos y descuentos
   - Salario neto

2. **Planilla Mensual Consolidada** (PDF)
   - Resumen de liquidaciones
   - Total de ingresos y descuentos
   - Comparativas

3. **Contrato de Trabajo** (PDF)
   - Información del empleado
   - Términos y condiciones
   - Firma digital

## 🤝 Funcionalidades por Rol

### RRHH (Administrador)
- Gestión completa de empleados
- CRUD de cargos
- Revisión y aprobación de permisos
- Registro de sanciones
- Generación de liquidaciones
- Acceso a bitácora
- Descarga de reportes

### Asistente RRHH
- Registro de asistencia
- Solicitud de permisos
- Cambio de contraseña
- Ver datos propios

## 🐛 Troubleshooting

### Error de conexión a PostgreSQL
```
Solución: Verificar que PostgreSQL esté corriendo y la contraseña sea correcta
```

### Error al generar PDFs
```
Solución: Instalar reportlab: pip install reportlab
```

### Puerto 5000 en uso
```
Solución: Cambiar puerto en run.py o parar proceso
```

## 📝 Notas Importantes

- Los permisos se almacenan como estados (PENDIENTE, APROBADO, RECHAZADO)
- Las vacaciones se calculan basadas en años
- El aporte IPS es automático del 9.625%
- La bitácora registra IP y User Agent
- Los PDFs se generan bajo demanda

## 🔧 Scripts de Mantenimiento

### Auditoría y Verificación
- `scripts/auditoria_anticipos.py` - Audita anticipos no descontados en liquidaciones
- `scripts/verificar_anticipo.py` - Verifica estado de un anticipo específico
- `sql/auditoria_anticipos.sql` - Queries SQL para auditoría manual

### Utilidades
- `scripts/generar_datos_prueba.py` - Genera datos de prueba
- `scripts/test_liquidaciones.py` - Prueba generación de liquidaciones
- `scripts/auto_renew_contracts.py` - Renueva contratos automáticamente

### Migraciones (Ya Aplicadas)
- `migrations/add_anticipos.py` - Agrega tabla de anticipos
- `migrations/add_bonificacion_familiar.py` - Bonificación familiar
- `migrations/add_justificacion_asistencia.py` - Justificaciones
- `migrations/add_despido_table.py` - Tabla de despidos

## 🚀 Deployment

Para producción:
1. Cambiar `FLASK_ENV` a `production`
2. Usar un servidor WSGI (Gunicorn, uWSGI)
3. Configurar reverse proxy (Nginx, Apache)
4. Usar certificado SSL/TLS
5. Configurar backup automático de PostgreSQL
6. Aumentar timeouts y límites
7. Habilitar logs de producción

## 📖 Documentación Adicional

- `docs/IMPLEMENTACION_COMPLETA.md` - Guía de implementación de anticipos
- `docs/ANALISIS_LIQUIDACION_COMPLETO.md` - Análisis del sistema de liquidación
- `docs/FIX_ANTICIPOS_LIQUIDACION.md` - Fix crítico de anticipos
- `docs/RESUMEN_EJECUTIVO_AUDITORIA.md` - Resumen de auditoría
- `SETUP_POSTGRESQL.md` - Configuración de PostgreSQL
- `MIGRACION_GUIA.md` - Guía de migración

## 📞 Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

**Desarrollado para la Cooperativa - 2025**
**Última actualización: Diciembre 2025**

## ✨ Nuevas Funcionalidades (Diciembre 2025)

### Sistema de Contratación de Postulantes
- ✅ Modal inteligente con auto-completado
- ✅ Generación automática de código empleado (EMP-001, EMP-002...)
- ✅ Validación de duplicados (CI, email, código)
- ✅ Mapeo postulante → empleado con preservación de datos
- ✅ Vinculación bidireccional automática
- ✅ Bitacora completa de contrataciones

### Identidad Corporativa
- ✅ Logo empresarial en login (sin autenticación)
- ✅ Logo en navbar de todas las páginas
- ✅ Header empresarial en dashboard con datos completos
- ✅ Membrete con logo en todos los PDFs (recibos, planillas)
- ✅ Fallback elegante con iniciales si no hay logo
- ✅ Configuración de empresa con upload de logo

### Mejoras UX/UI
- ✅ Diseño profesional con gradientes y sombras
- ✅ Validaciones JavaScript en tiempo real
- ✅ Mensajes descriptivos de error
- ✅ Responsive design mejorado
- ✅ Iconos y emojis contextuales
