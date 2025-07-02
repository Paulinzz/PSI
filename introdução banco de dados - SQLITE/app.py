import sqlite3

DATABASE = 'banco.sql'

conn = sqlite3.connect('banco.db')

with open (DATABASE) as f:
    conn.executescript(f.read())
    
conn.commit()
conn.close()