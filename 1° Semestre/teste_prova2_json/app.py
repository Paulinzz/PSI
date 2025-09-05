
from flask import Flask, render_template, redirect, request, url_for, session, flash, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.secret_key = 'super-secret-json'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

USUARIOS_ARQ = 'usuarios.json'
TAREFAS_ARQ = 'tarefas.json'

class Usuario(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    usuarios = ler_json(USUARIOS_ARQ)
    if user_id in usuarios:
        return Usuario(user_id)
    return None

def ler_json(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return {}
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4)

@app.route('/')
def index():
    nome = request.cookies.get('nome', 'Visitante')
    return render_template('index.html', nome=nome)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = generate_password_hash(request.form['senha'])

        usuarios = ler_json(USUARIOS_ARQ)
        if nome in usuarios:
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('cadastro'))

        usuarios[nome] = {'senha': senha}
        salvar_json(USUARIOS_ARQ, usuarios)

        tarefas = ler_json(TAREFAS_ARQ)
        tarefas[nome] = []
        salvar_json(TAREFAS_ARQ, tarefas)

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        usuarios = ler_json(USUARIOS_ARQ)
        user = usuarios.get(nome)
        if user and check_password_hash(user['senha'], senha):
            login_user(Usuario(nome))
            resp = make_response(redirect(url_for('tarefas')))
            resp.set_cookie('nome', nome)
            return resp

        flash('Credenciais inválidas', 'danger')
    return render_template('login.html')

@app.route('/tarefas', methods=['GET', 'POST'])
@login_required
def tarefas():
    tarefas = ler_json(TAREFAS_ARQ)
    user = current_user.id

    if request.method == 'POST':
        nova = request.form['tarefa']
        tarefas[user].append(nova)
        salvar_json(TAREFAS_ARQ, tarefas)
        flash('Tarefa adicionada!', 'success')

    return render_template('tarefas.html', tarefas=tarefas[user])

@app.route('/remover/<int:indice>')
@login_required
def remover(indice):
    tarefas = ler_json(TAREFAS_ARQ)
    user = current_user.id

    try:
        tarefas[user].pop(indice)
        salvar_json(TAREFAS_ARQ, tarefas)
        flash('Tarefa removida.', 'info')
    except:
        flash('Erro ao remover tarefa.', 'danger')

    return redirect(url_for('tarefas'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
