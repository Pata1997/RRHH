# 🎯 RESPUESTA DIRECTA: ¿QUÉ DEBE ESTAR EN LA RAÍZ?

## ARCHIVOS IMPRESCINDIBLES EN RAÍZ

```
SÍ O SÍ AQUÍ (No se pueden mover):

.env                    ← Flask lo busca aquí automáticamente
run.py                  ← Punto de entrada (python run.py)
requirements.txt        ← pip install -r requirements.txt
.gitignore              ← Git lo busca aquí automáticamente
.env.example            ← Template del .env
```

**Si los mueves:** ❌ El sistema no funciona

---

## ARCHIVOS RECOMENDADOS EN RAÍZ

```
MEJOR DEJARLOS AQUÍ (convención de GitHub):

README.md               ← GitHub muestra esto automáticamente
LICENSE                 ← GitHub muestra esto automáticamente
setup_postgres.py       ← Script importante de setup
init_database.py        ← Script importante de inicialización
clean_database.py       ← Script importante de limpieza
```

**Si los mueves:** ⚠️ Funcionan pero se ve desorganizado

---

## ARCHIVOS QUE SÍ PUEDEN MOVERSE

```
ESTOS SÍ PUEDEN IR A /docs (son documentación):

START_AQUI.txt
INSTALACION.txt
FLUJO_AUTOMATICO_LIQUIDACIONES.md
MEJORA_LIQUIDACIONES_AUTOMATICAS.md
COMO_FUNCIONA_AGUINALDO.md
DESPIDOS_IMPLEMENTACION.md
(+ todos los demás .md y .txt)

TOTAL: ~20-25 archivos de documentación
```

**Si los mueves:** ✅ Sin problemas

---

## ARCHIVOS A BORRAR

```
Estos son obsoletos, puedes borrarlos:

CHANGELOG_CORRECCIONES.txt
NOTAS.txt
ACCION_INMEDIATA.txt
AGUINALDOS_SIGUIENTE_PASO.txt
EJECUTAR_VISUAL.txt
INSTRUCCIONES_FINALES.txt
SOLO_EJECUTA_ESTO.md
RESUMEN_FINAL.md
VERIFICACION.txt

TOTAL: 9 archivos a eliminar
```

---

## ESTRUCTURA FINAL PROPUESTA

```
RRHH2/
│
├── 📄 .env                      ← RAÍZ (imprescindible)
├── 📄 .env.example              ← RAÍZ (imprescindible)
├── 📄 .gitignore                ← RAÍZ (imprescindible)
├── 📄 README.md                 ← RAÍZ (recomendado)
├── 📄 requirements.txt           ← RAÍZ (imprescindible)
├── 📄 run.py                    ← RAÍZ (imprescindible)
├── 📄 setup_postgres.py         ← RAÍZ (recomendado)
├── 📄 init_database.py          ← RAÍZ (recomendado)
├── 📄 clean_database.py         ← RAÍZ (recomendado)
│
├── 📁 docs/                     ← NUEVA (toda documentación)
│   ├── inicio/
│   │   ├── START_AQUI.txt
│   │   ├── COMIENZA_AQUI.txt
│   │   └── README.md
│   ├── ejecucion/
│   │   ├── INSTALACION.txt
│   │   ├── SETUP_POSTGRESQL.md
│   │   └── GUIA_COMPLETA_PROBAR_SISTEMA.md
│   ├── features/
│   │   ├── FLUJO_AUTOMATICO_LIQUIDACIONES.md
│   │   ├── MEJORA_LIQUIDACIONES_AUTOMATICAS.md
│   │   ├── COMO_FUNCIONA_AGUINALDO.md
│   │   └── DESPIDOS_IMPLEMENTACION.md
│   ├── testing/
│   │   ├── GUIA_GENERAR_DATOS_PRUEBA.md
│   │   └── VISUALIZACION_DATOS_SCRIPT.md
│   ├── tecnico/
│   │   ├── IMPLEMENTACION_COMPLETA_DESPIDOS_AGUINALDOS.md
│   │   └── CONVERSACION_IMPLEMENTACION.md
│   ├── referencias/
│   │   ├── INDICE_DOCUMENTACION.md
│   │   └── STATUS.txt
│   └── README.md
│
├── 📁 app/
├── 📁 scripts/
├── 📁 migrations/
├── 📁 tests/
├── 📁 instance/
└── 📁 venv/
```

---

## 📊 RESUMEN

| Ubicación | Cantidad | Ejemplos |
|-----------|----------|----------|
| **RAÍZ (imprescindible)** | 5 | .env, run.py, requirements.txt |
| **RAÍZ (recomendado)** | 4 | README.md, setup_postgres.py |
| **DOCS/** | 25 | Todo lo demás .md y .txt |
| **BORRAR** | 9 | Archivos obsoletos |

---

## ✨ CONCLUSIÓN

**En RAÍZ necesitas:**
- ✅ .env
- ✅ .env.example
- ✅ .gitignore
- ✅ run.py
- ✅ requirements.txt
- ✅ README.md (principal)

**Todo lo demás puede ir a `/docs`**

¿Hacemos la migración? 🚀

