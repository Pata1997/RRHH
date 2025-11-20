import psycopg2
conn = psycopg2.connect(dbname='rrhh_db', user='postgres', password='root', host='localhost', port='5432')
cur = conn.cursor()
cur.execute(\
UPDATE
usuarios
SET
rol
=
ADMIN
WHERE
nombre_usuario
=
admin
\)
conn.commit()
print('OK - Rol actualizado')
cur.execute(\SELECT
nombre_usuario
rol
FROM
usuarios
WHERE
nombre_usuario
=
admin
\)
result = cur.fetchone()
print(f'Usuario: {result[0]}, Rol: {result[1]}')
cur.close()
conn.close()
