# 🐘 Setup PostgreSQL para RRHH 2.0

Sigue estos pasos **en orden** para crear la base de datos y usuario en PostgreSQL.

## Opción 1: Usando psql (línea de comandos) ⭐ RECOMENDADO

### Paso 1: Abre psql
```powershell
psql -U postgres
```

Se te pedirá la contraseña de PostgreSQL (la que pusiste cuando instalaste PostgreSQL).

### Paso 2: Copia y pega estos comandos (uno por uno):

```sql
-- Crear la base de datos
CREATE DATABASE rrhh_db;

-- Crear el usuario
CREATE USER rrhh_user WITH PASSWORD '123456';

-- Configurar encoding
ALTER ROLE rrhh_user SET client_encoding TO 'utf8';
ALTER ROLE rrhh_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE rrhh_user SET default_transaction_deferrable TO on;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE rrhh_db TO rrhh_user;

-- Salir
\q
```

**Resultado esperado:** Sin errores, solo mensajes como "CREATE DATABASE" y "GRANT".

---

## Opción 2: Usando pgAdmin (interfaz gráfica)

1. Abre **pgAdmin** (debería estar en tu menú Inicio)
2. Login con tu contraseña
3. En el árbol izquierdo: **Servers** → **PostgreSQL** → botón derecho en **Databases**
4. Selecciona **Create** → **Database**
5. Rellena:
   - **Database name:** `rrhh_db`
   - **Owner:** (dejarlo en blanco o seleccionar `postgres`)
   - Click **Save**

6. Luego crea el usuario:
   - En el árbol: **Servers** → **PostgreSQL** → botón derecho en **Login/Group Roles**
   - Selecciona **Create** → **Login/Group Role**
   - Rellena:
     - **Name:** `rrhh_user`
     - Pestaña **Definition**: Password = `123456`
     - Pestaña **Privileges**: Marcar todas las opciones
     - Click **Save**

---

## Verificación

Después de crear BD y usuario, verifica que funciona:

```powershell
psql -U rrhh_user -d rrhh_db -h localhost
```

Si puedes conectar, verás el prompt `rrhh_db=>`. Luego escribe `\q` para salir.

---

## Si hay error de contraseña

Si psql pide contraseña y no la pide en el comando, crea un archivo `.pgpass` en `%APPDATA%\postgresql\pgpass.conf`:

```
localhost:5432:rrhh_db:rrhh_user:123456
```

Guarda el archivo en UTF-8 sin BOM.

---

**Una vez termines estos pasos, regresa aquí y te indicaré los siguientes comandos.**
