@echo off
REM Script de instalación y ejecución del Sistema RRHH
REM Compatible con Windows PowerShell y CMD

setlocal enabledelayedexpansion

echo ===============================================
echo    INSTALACION Y EJECUCION - SISTEMA RRHH
echo ===============================================
echo.

REM Verificar si está activado el entorno virtual
if not defined VIRTUAL_ENV (
    echo [1/6] Activando entorno virtual...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: No se pudo activar el entorno virtual
        echo Ejecutar primero: python -m venv venv
        pause
        exit /b 1
    )
    echo OK: Entorno virtual activado
) else (
    echo OK: Entorno virtual ya activo (%VIRTUAL_ENV%)
)
echo.

REM Instalar dependencias
echo [2/6] Verificando dependencias...
pip list | find /I "flask" >nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudo instalar las dependencias
        pause
        exit /b 1
    )
    echo OK: Dependencias instaladas
) else (
    echo OK: Dependencias ya instaladas
)
echo.

REM Crear archivo .env si no existe
echo [3/6] Verificando archivo .env...
if not exist .env (
    echo Creando archivo .env desde .env.example...
    if exist .env.example (
        copy .env.example .env
        echo OK: Archivo .env creado
        echo IMPORTANTE: Edita .env y configura DATABASE_URL
    ) else (
        echo ERROR: No encontrado .env.example
        pause
        exit /b 1
    )
) else (
    echo OK: Archivo .env ya existe
)
echo.

REM Inicializar base de datos
echo [4/6] Inicializando base de datos...
echo.
python init_database.py
if errorlevel 1 (
    echo ERROR: No se pudo inicializar la base de datos
    echo Verifica que PostgreSQL esté corriendo y que .env sea correcto
    pause
    exit /b 1
)
echo.

REM Mostrar información final
echo [5/6] Informacion final:
echo.
echo ========== USUARIOS DE PRUEBA ==========
echo Usuario: admin
echo Contraseña: admin123
echo Rol: RRHH (Administrador)
echo.
echo Usuario: asistente
echo Contraseña: asistente123
echo Rol: Asistente RRHH
echo.
echo ======== NUEVAS FUNCIONALIDADES ========
echo + Sistema de contratacion de postulantes
echo + Logo empresarial en login/dashboard/PDFs
echo + Validaciones de duplicados mejoradas
echo + Membretes profesionales en reportes
echo ========================================
echo.

REM Preguntar si ejecutar la aplicación
echo [6/6] Iniciando aplicación...
echo.
echo Ejecutando: python run.py
echo Accede en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python run.py

endlocal
