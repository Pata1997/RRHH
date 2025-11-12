# 📍 ARCHIVOS QUE DEBEN ESTAR EN LA RAÍZ

## Archivos por categoría

### 🔴 IMPRESCINDIBLES EN RAÍZ (No pueden moverse)

Estos archivos **DEBEN estar en la raíz** porque:

| Archivo | Razón | Consecuencia si se mueve |
|---------|-------|--------------------------|
| **.env** | Configuración de Flask | Flask no lo encuentra ❌ |
| **run.py** | Punto de entrada | `python run.py` no funciona ❌ |
| **requirements.txt** | Dependencias Python | `pip install -r requirements.txt` no funciona ❌ |
| **.env.example** | Template de .env | Referencia para usuario ❌ |

**¿Por qué?** Son detectados **automáticamente por el sistema** en la raíz.

---

### 🟡 ALTAMENTE RECOMENDADOS EN RAÍZ (Convención)

Estos archivos es mejor dejarlos en raíz por **convención de GitHub/proyectos profesionales:**

| Archivo | Razón | Se puede mover |
|---------|-------|----------------|
| **README.md** | Descripción del proyecto | ⚠️ Técnicamente sí, pero NO recomendado |
| **.gitignore** | Qué no trackear | ⚠️ Sí, pero Git lo busca primero en raíz |
| **LICENSE** | Licencia del proyecto | ⚠️ Sí, pero convención es raíz |

**¿Por qué?** GitHub/GitLab buscan estos archivos automáticamente en raíz.

---

### 🟢 PUEDEN MOVERSE (Documentación)

Todos los `.md` y `.txt` de **DOCUMENTACIÓN** pueden moverse a `/docs`:

```
✅ PUEDEN IR A /docs:

START_AQUI.txt
COMIENZA_AQUI.txt
INSTALACION.txt
SETUP_POSTGRESQL.md
COMO_EJECUTAR_MIGRACION.md
GUIA_COMPLETA_PROBAR_SISTEMA.md
FLUJO_AUTOMATICO_LIQUIDACIONES.md
MEJORA_LIQUIDACIONES_AUTOMATICAS.md
COMO_FUNCIONA_AGUINALDO.md
AGUINALDOS_MANUAL_RAPIDO.md
NAVEGACION_AGUINALDOS_VISUAL.md
DESPIDOS_IMPLEMENTACION.md
GUIA_GENERAR_DATOS_PRUEBA.md
VISUALIZACION_DATOS_SCRIPT.md
IMPLEMENTACION_COMPLETA_DESPIDOS_AGUINALDOS.md
IMPLEMENTACION_FINAL_VISUAL.md
CONVERSACION_IMPLEMENTACION.md
AGUINALDOS_RESUMEN_IMPLEMENTACION.md
INDICE_DOCUMENTACION.md
STATUS.txt
RESUMEN.txt
RESUMEN_PRUEBAS_EJECUTIVO.txt
CLASIFICACION_SIMPLIFICADA.md
GUIA_ARCHIVOS_DOCUMENTACION.md
RESPUESTA_ARCHIVOS_DOCUMENTACION.md
(+ otros)

TOTAL: ~20-25 archivos pueden moverse
```

---

## 📊 ANÁLISIS DETALLADO

### Imprescindibles (.env, run.py, requirements.txt)

```python
# run.py (línea 1-5)
import os
from dotenv import load_dotenv

load_dotenv()  # ← Busca .env en RAÍZ
app = create_app(os.environ.get('FLASK_ENV', 'development'))
```

Si .env no está en raíz:
```
❌ dotenv no lo encuentra
❌ Variables de entorno no cargan
❌ App no inicia
```

---

### Convención de GitHub

Cuando abres un proyecto en GitHub, busca:
```
README.md          ← Para mostrar descripción
.gitignore         ← Para ignorar archivos
LICENSE            ← Para mostrar licencia
requirements.txt   ← Para mostrar dependencias
```

Si los mueves a `/docs`:
```
⚠️ GitHub no los muestra automáticamente
⚠️ Usuario nuevo no ve qué es el proyecto
⚠️ Se ve desorganizado
```

---

## 🎯 RECOMENDACIÓN FINAL

### ✅ DEJAR EN RAÍZ:

```
RRHH2/
├── .env                    ← Imprescindible
├── .env.example            ← Convención
├── .gitignore              ← Convención
├── README.md               ← Convención
├── LICENSE                 ← Convención (si existe)
├── requirements.txt        ← Convención
├── run.py                  ← Imprescindible
├── setup_postgres.py       ← Script principal
├── init_database.py        ← Script principal
├── clean_database.py       ← Script principal
└── (archivos obsoletos que vas a borrar)
```

**Total: 10-12 archivos en raíz** (código + configuración)

---

### ✅ MOVER A /docs:

```
RRHH2/docs/
├── inicio/
│   ├── START_AQUI.txt
│   ├── COMIENZA_AQUI.txt
│   └── README.md (índice de inicio)
├── ejecucion/
│   ├── INSTALACION.txt
│   ├── SETUP_POSTGRESQL.md
│   ├── COMO_EJECUTAR_MIGRACION.md
│   └── GUIA_COMPLETA_PROBAR_SISTEMA.md
├── features/
│   ├── FLUJO_AUTOMATICO_LIQUIDACIONES.md
│   ├── MEJORA_LIQUIDACIONES_AUTOMATICAS.md
│   ├── COMO_FUNCIONA_AGUINALDO.md
│   └── (otros)
├── testing/
│   ├── GUIA_GENERAR_DATOS_PRUEBA.md
│   └── VISUALIZACION_DATOS_SCRIPT.md
├── tecnico/
│   ├── IMPLEMENTACION_COMPLETA_DESPIDOS_AGUINALDOS.md
│   └── (otros)
├── referencias/
│   ├── INDICE_DOCUMENTACION.md
│   └── STATUS.txt
└── README.md (índice de todas las docs)
```

**Total: ~20-25 archivos de documentación** (mejor organizados)

---

## 🗑️ BORRAR (Obsoletos):

```
CHANGELOG_CORRECCIONES.txt          ← Histórico
NOTAS.txt                           ← Notas temporales
ACCION_INMEDIATA.txt                ← Obsoleto
AGUINALDOS_SIGUIENTE_PASO.txt       ← Obsoleto
EJECUTAR_VISUAL.txt                 ← Obsoleto
INSTRUCCIONES_FINALES.txt           ← Obsoleto
SOLO_EJECUTA_ESTO.md                ← Obsoleto
RESUMEN_FINAL.md                    ← Duplicado
VERIFICACION.txt                    ← Parcial obsoleto

TOTAL: 9 archivos a eliminar
```

---

## 📋 ESTRUCTURA FINAL RECOMENDADA

```
RRHH2/
│
├── 📁 app/                          [CÓDIGO FUENTE]
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── bitacora.py
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── reports/
│
├── 📁 scripts/                      [SCRIPTS PYTHON]
│   ├── generar_datos_prueba.py
│   └── test_liquidaciones.py
│
├── 📁 tests/                        [TESTS UNITARIOS]
│   └── test_*.py
│
├── 📁 migrations/                   [MIGRACIONES BD]
│   └── add_despido_table.py
│
├── 📁 docs/                         [DOCUMENTACIÓN] ← NUEVA
│   ├── inicio/
│   │   ├── START_AQUI.txt
│   │   ├── COMIENZA_AQUI.txt
│   │   └── README.md
│   ├── ejecucion/
│   │   ├── INSTALACION.txt
│   │   ├── SETUP_POSTGRESQL.md
│   │   ├── COMO_EJECUTAR_MIGRACION.md
│   │   └── GUIA_COMPLETA_PROBAR_SISTEMA.md
│   ├── features/
│   │   ├── FLUJO_AUTOMATICO_LIQUIDACIONES.md
│   │   ├── MEJORA_LIQUIDACIONES_AUTOMATICAS.md
│   │   ├── COMO_FUNCIONA_AGUINALDO.md
│   │   ├── DESPIDOS_IMPLEMENTACION.md
│   │   └── README.md
│   ├── testing/
│   │   ├── GUIA_GENERAR_DATOS_PRUEBA.md
│   │   └── VISUALIZACION_DATOS_SCRIPT.md
│   ├── tecnico/
│   │   ├── IMPLEMENTACION_COMPLETA_DESPIDOS_AGUINALDOS.md
│   │   ├── CONVERSACION_IMPLEMENTACION.md
│   │   └── README.md
│   ├── referencias/
│   │   ├── INDICE_DOCUMENTACION.md
│   │   └── STATUS.txt
│   └── README.md (índice maestro de docs)
│
├── 📁 instance/                     [BD LOCAL]
├── 📁 venv/                         [ENTORNO VIRTUAL]
│
├── .env                             [CONFIGURACIÓN - NO TRACKEAR]
├── .env.example                     [TEMPLATE .env]
├── .gitignore                       [QUÉ NO TRACKEAR]
├── README.md                        [DESCRIPCIÓN DEL PROYECTO]
├── requirements.txt                 [DEPENDENCIAS]
├── run.py                           [PUNTO DE ENTRADA]
├── setup_postgres.py                [SETUP BD]
├── init_database.py                 [INICIALIZAR BD]
└── clean_database.py                [LIMPIAR BD]

RAÍZ: 12 archivos (código + config + scripts principales)
DOCS: 25 archivos (documentación)
TOTAL: 37 archivos importantes
```

---

## 📊 COMPARATIVA ANTES vs DESPUÉS

### ANTES (Desordenado):

```
RRHH2/ (raíz)
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── START_AQUI.txt              ← Documentación en raíz
├── COMIENZA_AQUI.txt           ← Documentación en raíz
├── INSTALACION.txt             ← Documentación en raíz
├── SETUP_POSTGRESQL.md         ← Documentación en raíz
├── COMO_EJECUTAR_MIGRACION.md  ← Documentación en raíz
├── FLUJO_AUTOMATICO...md       ← Documentación en raíz
├── (20+ más archivos .md/.txt) ← CAOS
├── CHANGELOG_CORRECCIONES.txt  ← OBSOLETO
├── NOTAS.txt                   ← OBSOLETO
├── app/
├── scripts/
└── migrations/

PROBLEMA: 30+ archivos en raíz, no se ve nada
```

### DESPUÉS (Ordenado):

```
RRHH2/ (raíz)
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── setup_postgres.py
├── init_database.py
├── clean_database.py
├── docs/                    ← Toda documentación aquí
│   ├── inicio/
│   ├── ejecucion/
│   ├── features/
│   ├── testing/
│   ├── tecnico/
│   ├── referencias/
│   └── README.md
├── app/
├── scripts/
└── migrations/

BENEFICIO: Raíz limpia, documentación organizada
```

---

## ✨ RESUMEN FINAL

### 🔴 SÍ O SÍ EN RAÍZ (Imprescindible):
```
.env
.env.example
.gitignore
run.py
requirements.txt
```

### 🟡 MEJOR EN RAÍZ (Convención):
```
README.md          (descripción proyecto)
LICENSE            (si existe)
setup_postgres.py  (script importante)
init_database.py   (script importante)
clean_database.py  (script importante)
```

### 🟢 PUEDEN IR A /docs:
```
Todos los demás .md y .txt (20-25 archivos)
```

### 🗑️ BORRAR:
```
9 archivos obsoletos
```

---

## 🎯 MI RECOMENDACIÓN

**Estructura final limpia:**

```
RRHH2/
├── Archivos de config (8-10 archivos)
├── docs/ (25 archivos de documentación organizados)
├── app/ (código)
├── scripts/ (scripts)
└── (resto)
```

**Resultado:**
- ✅ Raíz limpia
- ✅ Documentación organizada
- ✅ Profesional
- ✅ Fácil de navegar

¿Te parece bien? ¿Hacemos la migración?

