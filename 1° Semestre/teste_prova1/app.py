
from flask import Flask, render_template, redirect, request, url_for, session, flash, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

usuarios = {}
tarefas_por_usuario = {}

class Usuario(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

@app.route('/')
def index():
    nome = request.cookies.get('nome', 'Visitante')
    return render_template('index.html', nome=nome)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = generate_password_hash(request.form['senha'])
        usuarios[nome] = {'senha': senha}
        tarefas_por_usuario[nome] = []
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = usuarios.get(nome)
        if user and check_password_hash(user['senha'], senha):
            login_user(Usuario(nome))
            resp = make_response(redirect(url_for('tarefas')))
            resp.set_cookie('nome', nome)
            return resp
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/tarefas', methods=['GET', 'POST'])
@login_required
def tarefas():
    if request.method == 'POST':
        nova = request.form['tarefa']
        tarefas_por_usuario[current_user.id].append(nova)
        flash('Tarefa adicionada!', 'success')
    lista = tarefas_por_usuario[current_user.id]
    return render_template('tarefas.html', tarefas=lista)

@app.route('/remover/<int:indice>')
@login_required
def remover(indice):
    try:
        tarefas_por_usuario[current_user.id].pop(indice)
        flash('Tarefa removida!', 'info')
    except:
        flash('Erro ao remover.', 'danger')
    return redirect(url_for('tarefas'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout efetuado!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
