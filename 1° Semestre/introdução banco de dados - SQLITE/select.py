import sqlite3

conn = sqlite3.connect('banco.db')
conn.row_factory = sqlite3.Row

res = conn.execute('select * from users')
lista = res.fetchall()

for obj in lista:
    print()
conn.close()
