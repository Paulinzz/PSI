from flask import Flask, render_template
from flask import url_for, request, flash

from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from flask import session, redirect
from modelos import User

from modelos import User

login_manager = LoginManager() 
app = Flask(__name__)
app.secret_key = 'guilherme'
login_manager.init_app(app)
login_manager.login_view = 'login'
 

eventos = {}


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if 'usuarios' not in session:
        usuarios = {}
        session['usuarios'] = usuarios
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        email = request.form['email']
        senha= request.form['senha']
        l_usuarios = session.get('usuarios')
        if email in l_usuarios and senha == l_usuarios[email]: 
            user = User(nome=email, senha=senha)
            user.id = email
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Houve errro: senha ou login inválidos.', category='error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        senha= request.form['senha']
        #check
        usuarios = session.get('usuarios')
        if email not in usuarios.keys():
            usuarios[email] = senha
            session['usuarios'] = usuarios
            # logar
            user = User(email, senha)
            user.id = email
            print(usuarios)
            login_user(user)
            return redirect(url_for('login'))

        flash('Erro ao realizar cadastro', category='error')
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/dash', methods=['GET', 'POST'])
@login_required
def novo_evento():
    if request.method == "POST":
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = request.form['data']
        
        if not titulo or not descricao or not data:
            flash('Todos os campos são obrigatórios.', category='error')
            return redirect(url_for('new_event'))

        eventos = session.get('eventos', {})
        eventos[titulo] = {'descricao': descricao, 'data': data}
        session['eventos'] = eventos

        flash('Evento cadastrado com sucesso!', category='success')
        return redirect(url_for('events'))

    return render_template('dashboard.html')

@app.route('/events')
@login_required
def events():
    eventos = session.get('eventos', {})
    return render_template('events.html', eventos=eventos)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logout efetuado com sucesso!', 'info')
    return redirect(url_for('index'))


@app.route('/eventos-list', methods=['GET', 'POST'])
@login_required
def list_event():
    return render_template('eventos.html')