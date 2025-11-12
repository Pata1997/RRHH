#!/usr/bin/env powershell
# Script para mover documentacion a carpetas organizadas
# Uso: powershell -ExecutionPolicy Bypass -File mover_docs.ps1

$rootDir = "c:\Users\Informatica 1\Desktop\Proyectos\RRHH2"
$docsDir = "$rootDir\docs"

Write-Host "MIGRANDO DOCUMENTACION A /docs..." -ForegroundColor Green
Write-Host ""

# Función para mover archivo
function Mover-Archivo {
    param(
        [string]$archivo,
        [string]$destino,
        [string]$categoria
    )
    
    $origen = "$rootDir\$archivo"
    $dest_path = "$destino\$archivo"
    
    if (Test-Path $origen) {
        Move-Item -Path $origen -Destination $dest_path -Force
        Write-Host "$archivo moved to $categoria" -ForegroundColor Cyan
    } else {
        Write-Host "Not found: $archivo" -ForegroundColor Yellow
    }
}

# INICIO
Write-Host "Moviendo a docs/inicio..." -ForegroundColor Magenta
Mover-Archivo "START_AQUI.txt" "$docsDir\inicio" "inicio"
Mover-Archivo "COMIENZA_AQUI.txt" "$docsDir\inicio" "inicio"

# EJECUCION
Write-Host ""
Write-Host "Moviendo a docs/ejecucion..." -ForegroundColor Magenta
Mover-Archivo "INSTALACION.txt" "$docsDir\ejecucion" "ejecucion"
Mover-Archivo "SETUP_POSTGRESQL.md" "$docsDir\ejecucion" "ejecucion"
Mover-Archivo "COMO_EJECUTAR_MIGRACION.md" "$docsDir\ejecucion" "ejecucion"
Mover-Archivo "GUIA_COMPLETA_PROBAR_SISTEMA.md" "$docsDir\ejecucion" "ejecucion"

# FEATURES
Write-Host ""
Write-Host "Moviendo a docs/features..." -ForegroundColor Magenta
Mover-Archivo "FLUJO_AUTOMATICO_LIQUIDACIONES.md" "$docsDir\features" "features"
Mover-Archivo "MEJORA_LIQUIDACIONES_AUTOMATICAS.md" "$docsDir\features" "features"
Mover-Archivo "COMO_FUNCIONA_AGUINALDO.md" "$docsDir\features" "features"
Mover-Archivo "AGUINALDOS_MANUAL_RAPIDO.md" "$docsDir\features" "features"
Mover-Archivo "NAVEGACION_AGUINALDOS_VISUAL.md" "$docsDir\features" "features"
Mover-Archivo "AGUINALDOS_RESUMEN_IMPLEMENTACION.md" "$docsDir\features" "features"
Mover-Archivo "DESPIDOS_IMPLEMENTACION.md" "$docsDir\features" "features"

# TESTING
Write-Host ""
Write-Host "Moviendo a docs/testing..." -ForegroundColor Magenta
Mover-Archivo "GUIA_GENERAR_DATOS_PRUEBA.md" "$docsDir\testing" "testing"
Mover-Archivo "VISUALIZACION_DATOS_SCRIPT.md" "$docsDir\testing" "testing"

# TECNICO
Write-Host ""
Write-Host "Moviendo a docs/tecnico..." -ForegroundColor Magenta
Mover-Archivo "IMPLEMENTACION_COMPLETA_DESPIDOS_AGUINALDOS.md" "$docsDir\tecnico" "tecnico"
Mover-Archivo "IMPLEMENTACION_FINAL_VISUAL.md" "$docsDir\tecnico" "tecnico"
Mover-Archivo "CONVERSACION_IMPLEMENTACION.md" "$docsDir\tecnico" "tecnico"

# REFERENCIAS
Write-Host ""
Write-Host "Moviendo a docs/referencias..." -ForegroundColor Magenta
Mover-Archivo "INDICE_DOCUMENTACION.md" "$docsDir\referencias" "referencias"
Mover-Archivo "STATUS.txt" "$docsDir\referencias" "referencias"

# RESUMEN (también va a referencias)
Mover-Archivo "RESUMEN.txt" "$docsDir\referencias" "referencias"
Mover-Archivo "RESUMEN_PRUEBAS_EJECUTIVO.txt" "$docsDir\referencias" "referencias"

# BORRANDO OBSOLETOS
Write-Host ""
Write-Host "Borrando archivos obsoletos..." -ForegroundColor Red

$obsoletos = @(
    "CHANGELOG_CORRECCIONES.txt",
    "NOTAS.txt",
    "ACCION_INMEDIATA.txt",
    "AGUINALDOS_SIGUIENTE_PASO.txt",
    "EJECUTAR_VISUAL.txt",
    "INSTRUCCIONES_FINALES.txt",
    "SOLO_EJECUTA_ESTO.md",
    "RESUMEN_FINAL.md",
    "VERIFICACION.txt"
)

foreach ($archivo in $obsoletos) {
    $ruta = "$rootDir\$archivo"
    if (Test-Path $ruta) {
        Remove-Item -Path $ruta -Force
        Write-Host "Deleted: $archivo" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "MIGRACION COMPLETADA" -ForegroundColor Green
Write-Host ""
Write-Host "Resumen:" -ForegroundColor Cyan
Write-Host "  - Estructura /docs creada"
Write-Host "  - Documentos organizados"
Write-Host "  - Indices creados"
Write-Host "  - Archivos obsoletos eliminados"
Write-Host ""
Write-Host "Proximo paso: Lee docs/README.md" -ForegroundColor Yellow
