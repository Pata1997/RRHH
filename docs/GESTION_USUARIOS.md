# 👥 Módulo de Gestión de Usuarios

## 📋 Descripción

Módulo administrativo para la gestión completa de usuarios del sistema RRHH.

**Acceso:** Solo para usuarios con rol **ADMIN** 👑

## ✨ Funcionalidades

### 1️⃣ **Listar Usuarios**
- Ver todos los usuarios del sistema
- Información mostrada:
  - Nombre de usuario
  - Nombre completo
  - Email
  - Rol (ADMIN, RRHH, ASISTENTE_RRHH)
  - Estado (Activo/Inactivo)
  - Último login
  - Fecha de creación

### 2️⃣ **Crear Usuario**
- Formulario completo con validaciones
- Campos:
  - Nombre de usuario (alfanumérico + guión bajo)
  - Email (único)
  - Nombre completo
  - Contraseña (mínimo 6 caracteres)
  - Rol (ADMIN, RRHH, ASISTENTE_RRHH)
  - Estado inicial (Activo/Inactivo)
- Validaciones:
  - Usuario único
  - Email único
  - Contraseñas coincidentes
  - Longitud mínima de contraseña

### 3️⃣ **Editar Usuario**
- Modificar datos existentes
- Cambio opcional de contraseña
- No requiere contraseña si no se desea cambiar
- Ver información de creación y último login

### 4️⃣ **Eliminar Usuario**
- Confirmación con modal
- Protecciones:
  - No se puede eliminar a sí mismo
  - No se puede eliminar el último administrador
- Acción irreversible

### 5️⃣ **Activar/Desactivar Usuario**
- Toggle rápido de estado
- Usuario inactivo no puede iniciar sesión
- No se puede desactivar a sí mismo

## 🔐 Roles del Sistema

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| 👑 **ADMIN** | Administrador | Acceso total + gestión de usuarios |
| 👔 **RRHH** | Recursos Humanos | Gestión completa de RRHH (sin gestión de usuarios) |
| 📋 **ASISTENTE_RRHH** | Asistente | Consulta y operaciones básicas |

## 🚀 Cómo Usar

### Acceder al Módulo

1. Iniciar sesión como **ADMIN**
2. En el menú superior verás: **👥 Usuarios**
3. Click en **Usuarios** para ver la lista

### Crear un Usuario

1. Click en **➕ Nuevo Usuario**
2. Completar el formulario
3. Seleccionar el rol apropiado
4. Click en **Crear Usuario**

### Editar un Usuario

1. En la lista, click en el botón **✏️ Editar**
2. Modificar los campos necesarios
3. (Opcional) Cambiar contraseña
4. Click en **Guardar Cambios**

### Activar/Desactivar

1. En la lista, click en el botón **⚠️ Toggle Estado**
2. Confirma la acción
3. El usuario será activado/desactivado inmediatamente

### Eliminar un Usuario

1. En la lista, click en el botón **🗑️ Eliminar**
2. Confirmar en el modal
3. El usuario será eliminado permanentemente

## 🛡️ Seguridad

### Validaciones Implementadas

✅ Solo usuarios ADMIN pueden acceder  
✅ No se puede eliminar a sí mismo  
✅ No se puede desactivar a sí mismo  
✅ No se puede eliminar el último administrador  
✅ Usuarios únicos (no duplicados)  
✅ Emails únicos  
✅ Contraseñas hasheadas (bcrypt)  
✅ Validación de contraseñas coincidentes  
✅ Mínimo 6 caracteres en contraseñas  

### Registro en Bitácora

Todas las acciones quedan registradas:
- ✅ Creación de usuario
- ✅ Edición de usuario
- ✅ Eliminación de usuario
- ✅ Cambio de estado
- ✅ Visualización de lista

## 📱 Ubicación en el Sistema

**Ruta:** `/admin/usuarios`

**Menú:** Solo visible para rol ADMIN en el menú superior

## 🎨 Interfaz

- Tabla responsive con Bootstrap 5
- Badges de colores para roles y estados
- Modales de confirmación para acciones críticas
- Formularios con validación frontend y backend
- Iconos Bootstrap Icons
- Mensajes flash para feedback

## 📝 Notas Importantes

⚠️ **No hay usuario ADMIN por defecto**
- Debes crear uno manualmente en la base de datos o usar el script `run.py` que crea usuario `admin` con contraseña `admin123`

⚠️ **Contraseñas**
- Se almacenan hasheadas con bcrypt
- Nunca se muestran en texto plano
- En edición, dejar vacío para mantener la actual

⚠️ **Eliminación**
- Es permanente
- Se elimina en cascada la bitácora del usuario
- Asegúrate antes de confirmar

## 🔧 Archivos del Módulo

```
app/
├── routes/
│   └── admin.py              # Rutas administrativas
└── templates/
    └── admin/
        ├── usuarios.html          # Lista de usuarios
        ├── crear_usuario.html     # Formulario crear
        └── editar_usuario.html    # Formulario editar
```

## ✅ Funcionalidades Completadas

- [x] Listar usuarios con información completa
- [x] Crear nuevo usuario con validaciones
- [x] Editar usuario existente
- [x] Eliminar usuario con confirmación
- [x] Activar/Desactivar usuario
- [x] Control de acceso solo ADMIN
- [x] Validaciones de seguridad
- [x] Registro en bitácora
- [x] Interfaz responsive
- [x] Mensajes de feedback

---

**Última actualización:** 20/11/2025
