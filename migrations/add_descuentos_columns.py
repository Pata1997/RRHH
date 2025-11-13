#!/usr/bin/env python3
"""
Add missing columns to descuentos table.
Run: python migrations/add_descuentos_columns.py
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

ADD_COLUMNS_SQL = """
ALTER TABLE descuentos 
ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE;

ALTER TABLE descuentos 
ADD COLUMN IF NOT EXISTS origen_tipo VARCHAR(50);

ALTER TABLE descuentos 
ADD COLUMN IF NOT EXISTS origen_id INTEGER;
"""

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
try:
    # Execute each statement separately
    for stmt in ADD_COLUMNS_SQL.split(';'):
        stmt = stmt.strip()
        if stmt:
            cur.execute(stmt)
    conn.commit()
    print('Columns added to descuentos table successfully')
except Exception as e:
    conn.rollback()
    print('Error:', e)
    raise
finally:
    cur.close()
    conn.close()
