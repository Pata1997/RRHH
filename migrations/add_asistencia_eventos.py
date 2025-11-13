#!/usr/bin/env python3
"""
Idempotent migration: create asistencia_eventos table if not exists.
Run: python migrations/add_asistencia_eventos.py
"""
import os
import sys
import psycopg2
from psycopg2 import sql

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATABASE_URL = os.environ.get('DATABASE_URL')

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS asistencia_eventos (
    id serial PRIMARY KEY,
    empleado_id integer NOT NULL REFERENCES empleados(id),
    ts timestamp without time zone NOT NULL,
    tipo varchar(10) NOT NULL,
    origen varchar(50) DEFAULT 'web',
    detalles text,
    fecha_creacion timestamp without time zone DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_asistencia_eventos_empleado_ts ON asistencia_eventos (empleado_id, ts);
"""

if not DATABASE_URL:
    print('DATABASE_URL not set, skipping migration')
    exit(0)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
try:
    cur.execute(CREATE_SQL)
    conn.commit()
    print('asistencia_eventos table ensured')
except Exception as e:
    conn.rollback()
    print('Error:', e)
    raise
finally:
    cur.close()
    conn.close()
