import os # Ferramenta para mexer com arquivos do sistema
import sqlite3 # Ferramenta para mexer com bancos de dados SQLite

# Onde está o arquivo 'schema.sql'?
CAMINHO = os.path.dirname(__file__)
ARQUIVO_SCHEMA = os.path.join(CAMINHO, 'schema.sql')

# Abre o arquivo 'schema.sql' e lê seu conteúdo
with open(ARQUIVO_SCHEMA, 'r') as f:
    schema = f.read()

# Função para pegar uma "conexão" com o banco de dados
def obter_conexao():
    return sqlite3.connect('meubanco.db') # Conecta ou cria o arquivo do banco de dados

# Agora, realmente conectamos e executamos o projeto da fundação
con = sqlite3.connect('meubanco.db') # Abre a conexão
con.executescript(schema) # Roda os comandos do schema (cria a tabela)
con.commit() # Salva as mudanças
con.close() # Fecha a conexão