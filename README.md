# Sistema de Gestión de Recursos Humanos (RRHH) - Cooperativa

Una aplicación web completa para la gestión de recursos humanos desarrollada con **Flask**, **PostgreSQL** y **Bootstrap 5**.

## 🚀 Características Principales

### 1. **Gestión de Empleados**
- Registro, edición y eliminación de empleados
- Información personal y laboral completa
- Estados de empleado (Activo, Inactivo, Suspendido, Jubilado)
- Búsqueda y filtrado de empleados

### 2. **Gestión de Cargos**
- CRUD de cargos
- Salario base configurable por cargo
- Descripción de funciones

### 3. **Control de Asistencia**
- Registro de entrada/salida por código de empleado
- Interfaz simple para escaneo rápido
- Bitácora completa de asistencias
- Edición manual de registros

### 4. **Gestión de Permisos**
- Solicitud de permisos (enfermedad, asunto personal, etc.)
- Aprobación/rechazo de solicitudes
- Cálculo automático de días
- Historial de permisos

### 5. **Sanciones Disciplinarias**
- Registro de sanciones (amonestación, descuento, suspensión)
- Monto configurable
- Descripción y motivos

### 6. **Liquidación de Salarios (Nómina)**
- Generación automática de liquidaciones mensuales
- Cálculo de:
  - Salario base
  - Ingresos extras
  - Descuentos
  - Aporte IPS (9.625%)
  - Salario neto
- Generación de recibos en PDF
- Planilla consolidada mensual

### 7. **Gestión de Vacaciones**
- Solicitud de vacaciones
- Seguimiento de días disponibles, tomados y pendientes
- Aprobación de solicitudes

### 8. **Contratos**
- Generación de contratos en PDF con ReportLab
- Información del empleado y condiciones

### 9. **Reportes PDF**
- Recibo individual de salario
- Planilla de liquidación mensual
- Contrato de trabajo

### 10. **Bitácora de Auditoría**
- Registro de todas las acciones CRUD
- Información del usuario, fecha, hora y detalles
- Filtrado por usuario y módulo
- Trazabilidad completa del sistema

### 11. **Autenticación y Autorización**
- Sistema de login seguro
- Dos roles: RRHH y Asistente RRHH
- Control de acceso por roles
- Cambio de contraseña

### 12. **Interfaz Moderna**
- Bootstrap 5 responsivo
- DataTables para tablas interactivas
- SweetAlert2 para confirmaciones
- Alertas flash para retroalimentación
- Navbar con menús dinámicos

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
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticación**: Flask-Login
- **Reportes**: ReportLab
- **Frontend**: Bootstrap 5, DataTables, SweetAlert2
- **Python**: 3.8+

## 📦 Dependencias

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
psycopg2-binary==2.9.7
reportlab==4.0.7
python-dotenv==1.0.0
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
- **asistencias**: Registro de asistencia
- **permisos**: Solicitudes de permisos
- **sanciones**: Disciplina
- **liquidaciones**: Nómina
- **vacaciones**: Gestión de vacaciones
- **contratos**: Contratos de trabajo
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

## 🚀 Deployment

Para producción:
1. Cambiar `FLASK_ENV` a `production`
2. Usar un servidor WSGI (Gunicorn, uWSGI)
3. Configurar reverse proxy (Nginx, Apache)
4. Usar certificado SSL/TLS
5. Aumentar timeouts y límites

## 📞 Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

**Desarrollado para la Cooperativa - 2025**
