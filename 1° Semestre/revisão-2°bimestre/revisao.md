

-----

# Estrutura do Projeto Flask com Flask-Login e SQLite

Aqui estão os arquivos que compõem o sistema.

## 1\. `revisão-2°bimestre/schema.sql`

Este arquivo define a estrutura da sua tabela de usuários no banco de dados SQLite.

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);
```

## 2\. `revisão-2°bimestre/iniciar.py`

Este script é responsável por inicializar o banco de dados (`meubanco.db`) e criar a tabela `usuarios` de acordo com o `schema.sql`.

```python
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
```

## 3\. `revisão-2°bimestre/app.py`

Este é o arquivo principal do seu aplicativo Flask, onde as rotas, a lógica de negócio e a integração com o Flask-Login são definidas.

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from iniciar import obter_conexao


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_super_secreta_e_longa_aqui' # <<< MUITO IMPORTANTE: ALTERE ISSO!

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redireciona para esta view se não estiver logado

# Classe User para Flask-Login
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get(user_id):
        conn = obter_conexao()
        cursor = conn.execute("SELECT id, nome FROM usuarios WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(user_data[0], user_data[1])
        return None

    def get_id(self):
        return str(self.id)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # AVISO: NÃO USE SENHA EM TEXTO SIMPLES EM PRODUÇÃO!

        conn = obter_conexao()
        cursor = conn.execute("SELECT id, nome FROM usuarios WHERE nome = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # PARA DEMONSTRAÇÃO: assume que a senha é o mesmo que o username
            if username == password: # AVISO: Isso é inseguro, apenas para demonstração!
                user = User(user_data[0], user_data[1])
                login_user(user)
                flash('Logado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Nome de usuário ou senha inválidos', 'danger')
        else:
            flash('Nome de usuário ou senha inválidos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@login_required # Protege esta rota: exige que o usuário esteja logado
def index():
    if request.method == 'POST':
        name = request.form['name']
        
        conn = obter_conexao()
        cursor = conn.execute("SELECT id FROM usuarios WHERE nome = ?", (name,))
        existing_user = cursor.fetchone()
        if not existing_user:
            sql = "INSERT INTO usuarios(nome) VALUES (?)"
            conn.execute(sql, (name,))
            conn.commit()
            flash(f'Usuário {name} adicionado!', 'success')
        else:
            flash(f'Usuário {name} já existe!', 'warning')
        conn.close()
        
        return redirect(url_for('index'))
    
    conn = obter_conexao()
    sql = "SELECT id, nome FROM usuarios"
    lista_db = conn.execute(sql).fetchall()
    conn.close()

    lista = [{'id': row[0], 'nome': row[1]} for row in lista_db]
        
    return render_template('index.html', lista=lista)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # AVISO: NÃO USE SENHA EM TEXTO SIMPLES EM PRODUÇÃO!

        conn = obter_conexao()
        cursor = conn.execute("SELECT id FROM usuarios WHERE nome = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha um diferente.', 'danger')
        else:
            # PARA DEMONSTRAÇÃO: apenas armazena o username como "senha"
            sql = "INSERT INTO usuarios(nome) VALUES (?)"
            conn.execute(sql, (username,)) # AVISO: Inseguro para senhas!
            conn.commit()
            conn.close()
            flash('Registro bem-sucedido! Por favor, faça login.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')
```

## 4\. `revisão-2°bimestre/templates/index.html`

Este é o template da página inicial, que exibe informações dependendo do status de login do usuário.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class=flashes>
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}

    {% if current_user.is_authenticated %}
        <p>Olá {{ current_user.name }}!</p>
        <p><a href="{{ url_for('logout') }}">Sair</a></p>
        <form action="" method="post">
            <input type="text" name="name" placeholder="Nome">
            <button>Enviar</button>
        </form>

        <h2>Lista de Usuários:</h2>
        {% if lista %}
            <ul>
            {% for usuario in lista %}
                <li>
                    Olá {{ usuario.nome }}! (ID: {{ usuario.id }})
                </li>
            {% endfor %}
            </ul>
        {% else %}
            <p>Nenhum usuário na lista.</p>
        {% endif %}
    {% else %}
        <p>Você não está logado.</p>
        <p><a href="{{ url_for('login') }}">Entrar</a></p>
        <p><a href="{{ url_for('register') }}">Registrar</a></p>
    {% endif %}
    
</body>
</html>
```

## 5\. `revisão-2°bimestre/templates/login.html`

Este template contém o formulário para os usuários fazerem login.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class=flashes>
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    <form action="" method="post">
        <input type="text" name="username" placeholder="Nome de Usuário" required><br>
        <input type="password" name="password" placeholder="Senha" required><br>
        <button type="submit">Entrar</button>
    </form>
    <p>Não tem uma conta? <a href="{{ url_for('register') }}">Registre-se aqui</a></p>
</body>
</html>
```

## 6\. `revisão-2°bimestre/templates/register.html`

Este template contém o formulário para novos usuários se registrarem.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class=flashes>
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    <form action="" method="post">
        <input type="text" name="username" placeholder="Nome de Usuário" required><br>
        <input type="password" name="password" placeholder="Senha" required><br>
        <button type="submit">Registrar</button>
    </form>
    <p>Já tem uma conta? <a href="{{ url_for('login') }}">Faça login aqui</a></p>
</body>
</html>
```