#!/usr/bin/env python
"""Script para verificar todas las rutas registradas"""

from app import create_app

app = create_app()

print("\n=== TODAS LAS RUTAS REGISTRADAS ===\n")
for rule in app.url_map.iter_rules():
    if 'anticipos' in rule.rule:
        print(f"{rule.rule:50} {rule.methods}")

print("\n=== BUSCANDO /rrhh/anticipos/create ===\n")
found = False
for rule in app.url_map.iter_rules():
    if rule.rule == '/rrhh/anticipos/create':
        print(f"✓ ENCONTRADA: {rule.rule}")
        print(f"  Métodos: {rule.methods}")
        print(f"  Endpoint: {rule.endpoint}")
        found = True

if not found:
    print("✗ NO ENCONTRADA la ruta /rrhh/anticipos/create")
