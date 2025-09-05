from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from users import User, users_db  # Módulo contendo a simulação do banco de dados de usuários

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura'  # Usada para proteger sessões e cookies

# Inicializa o gerenciador de login, gerenciar a autenticação dos usuários
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Página que será redirecionada se o usuário não estiver logado

# Carrega o usuário a partir do ID da sessão
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db:
            flash('Usuário já existe.')
            return redirect(url_for('register'))

        # Cria um novo usuário e adiciona no "banco de dados"
        new_user = User(id=username, password=password)
        users_db[username] = new_user
        flash('Cadastro realizado com sucesso. Faça login!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_db.get(username)

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required  # Garante que apenas usuários logados acessem
def dashboard():
    return render_template('dashboard.html', name=current_user.id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
