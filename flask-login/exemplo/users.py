from flask_login import UserMixin

# Classe de usuário que herda de UserMixin para integrar com flask-login
class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

# Simula um "banco de dados" simples com usuários
users_db = {}
