import sqlite3

conn = sqlite3.connect('banco.db')

# TESTE
sql = 'INSERT INTO livros(título, usuario_id) VALUES(EU, 100)'

conn.execute(sql)
conn.commit()
conn.close()