# init_db.py
import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    # Criar tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    ''')
    
    # Inserir usuário admin padrão (opcional)
    admin_email = "admin@example.com"
    admin_senha = generate_password_hash("senha_segura")
    
    cursor.execute('''
    INSERT OR IGNORE INTO users (email, senha) 
    VALUES (?, ?)
    ''', (admin_email, admin_senha))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")