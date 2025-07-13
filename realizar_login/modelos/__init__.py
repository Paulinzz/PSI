from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import obter_conexao

class User(UserMixin):
    def __init__(self, id, email, senha_hash):
        self.id = id
        self.email = email
        self.senha_hash = senha_hash
        
    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM users WHERE id = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        conexao.close()
        
        if resultado:
            return User(
                id=resultado['id'],
                email=resultado['email'],
                senha_hash=resultado['senha']
            )
        return None

    @classmethod
    def get_by_email(cls, email):
        conexao = obter_conexao()
        sql = "SELECT * FROM users WHERE email = ?"
        resultado = conexao.execute(sql, (email,)).fetchone()
        conexao.close()
        
        if resultado:
            return User(
                id=resultado['id'],
                email=resultado['email'],
                senha_hash=resultado['senha']
            )
        return None

    @classmethod
    def create(cls, email, senha):
        senha_hash = generate_password_hash(senha)
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO users (email, senha) VALUES (?, ?)",
            (email, senha_hash)
        )
        user_id = cursor.lastrowid
        conexao.commit()
        conexao.close()
        return cls.get(user_id)
    
    @classmethod
    def get_all(cls):
        conexao = obter_conexao()
        cursor = conexao.execute("SELECT * FROM users")
        usuarios = cursor.fetchall()
        conexao.close()
        return usuarios