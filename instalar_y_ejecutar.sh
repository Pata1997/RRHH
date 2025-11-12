#!/bin/bash
# Script de instalación y ejecución para Linux/Mac

echo "========================================"
echo "   INSTALACION Y EJECUCION - RRHH"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "[1/6] Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo crear el entorno virtual"
        exit 1
    fi
fi

# Activar entorno virtual
echo "[2/6] Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "[3/6] Instalando dependencias..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo instalar las dependencias"
    exit 1
fi

# Crear archivo .env
echo "[4/6] Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "IMPORTANTE: Edita .env y configura DATABASE_URL"
    fi
fi

# Inicializar base de datos
echo "[5/6] Inicializando base de datos..."
python init_database.py
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo inicializar la base de datos"
    exit 1
fi

# Información final
echo ""
echo "[6/6] Información final:"
echo ""
echo "======== USUARIOS DE PRUEBA ========"
echo "Usuario: admin"
echo "Contraseña: admin123"
echo "Rol: RRHH"
echo ""
echo "Usuario: asistente"
echo "Contraseña: asistente123"
echo "Rol: Asistente RRHH"
echo "======================================"
echo ""
echo "Ejecutando: python run.py"
echo "Accede en: http://localhost:5000"
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

# Ejecutar la aplicación
python run.py
