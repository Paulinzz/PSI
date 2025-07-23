import sqlite3

conn = sqlite3.connect('banco.db')
arq = 'schema.sql'

with open(arq) as f:
    conn.executescript(f.read())
    
conn.close()  