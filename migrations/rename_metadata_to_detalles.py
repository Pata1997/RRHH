#!/usr/bin/env python3
"""
Rename metadata column to detalles in asistencia_eventos table.
Run: python migrations/rename_metadata_to_detalles.py
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

if not DATABASE_URL:
    print('DATABASE_URL not set, skipping migration')
    sys.exit(0)

RENAME_SQL = """
ALTER TABLE asistencia_eventos RENAME COLUMN metadata TO detalles;
"""

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
try:
    cur.execute(RENAME_SQL)
    conn.commit()
    print('metadata column renamed to detalles successfully')
except Exception as e:
    conn.rollback()
    print('Error (may be already renamed):', e)
finally:
    cur.close()
    conn.close()
