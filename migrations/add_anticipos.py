#!/usr/bin/env python
"""Create anticipos table if not exists
"""
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print('DATABASE_URL not set in environment')
    exit(1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS anticipos (
    id SERIAL PRIMARY KEY,
    empleado_id INTEGER NOT NULL REFERENCES empleados(id),
    monto NUMERIC(12,2) NOT NULL,
    fecha_solicitud TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    aprobado BOOLEAN DEFAULT FALSE,
    aprobado_por INTEGER REFERENCES usuarios(id),
    fecha_aprobacion TIMESTAMP WITHOUT TIME ZONE,
    aplicado BOOLEAN DEFAULT FALSE,
    fecha_aplicacion DATE,
    justificativo_archivo VARCHAR(255),
    observaciones TEXT,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_anticipos_empleado ON anticipos(empleado_id);
""")

conn.commit()
cur.close()
conn.close()
print('anticipos table ensured')
