import os
import sqlite3

CAMINHO = os.path.dirname(__file__)  # Pega o caminho da pasta atual
ARQUIVO_SCHEMA = os.path.join(CAMINHO, 'schema.sql')

with open(ARQUIVO_SCHEMA, 'r') as f:
    schema = f.read()

def obter_conexao():
    return sqlite3.connect('meubanco.db')

con = sqlite3.connect('meubanco.db')
con.executescript(schema)
con.commit()
con.close()
