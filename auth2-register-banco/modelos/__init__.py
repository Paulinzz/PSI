# modelos.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import flash

class User(UserMixin):
    def __init__(self, id, email, senha_hash):
        self.id = id
        self.email = email
        self.senha_hash = senha_hash

    # UserMixin já fornece implementações padrão para:
    # is_authenticated, is_active, is_anonymous, get_id()
    
    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, senha FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(id=user_data[0], email=user_data[1], senha_hash=user_data[2])
        return None

    @staticmethod
    def get_by_email(email):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, senha FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(id=user_data[0], email=user_data[1], senha_hash=user_data[2])
        return None

    @staticmethod
    def all():
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users")
        users = cursor.fetchall()
        conn.close()
        return [{'id': user[0], 'email': user[1]} for user in users]

    @staticmethod
    def delete(user_id):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return False

    @staticmethod
    def create(email, senha):
        senha_hash = generate_password_hash(senha)
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, senha) VALUES (?, ?)",
                (email, senha_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return User(id=user_id, email=email, senha_hash=senha_hash)
        except sqlite3.IntegrityError:
            flash('Este email já está cadastrado.', 'error')
            return None
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def verify_password(self, senha):
        return check_password_hash(self.senha_hash, senha)