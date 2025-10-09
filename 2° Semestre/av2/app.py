# app.py (ou routes.py, conforme estrutura do projeto)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, LoginManager, logout_user
from models import User, Livro, SessionLocal, Base, engine
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'segredo123'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        user_data = session.get(User, user_id)
        if user_data:
            return user_data
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['senha'].strip()

        with SessionLocal() as session:
            with session.begin():
                # Verifica se o usuário já existe
                if session.query(User).where(User.email == email).first():
                    flash('Nome de usuário já está em uso.', 'warning')
                    return redirect(url_for('register'))

                # Cria novo usuário
                hashed_password = generate_password_hash(password)
                novo_user = User(email=email, password=hashed_password)
                session.add(novo_user)

            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['senha'].strip()

        with SessionLocal() as session:
            with session.begin():
                user = session.query(User).where(User.email == email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('listar_livros'))
            else:
                flash('Usuário ou senha incorretos.', 'danger')
                return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/profile')
@login_required
def profile():
    # Aqui, futuramente, o aluno pode adicionar relacionamento com posts, tarefas etc.
    return render_template('profile.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/livros')
@login_required
def listar_livros():
    
    with SessionLocal() as session:
        with session.begin():
            user = session.query(User).where(User.email == current_user.email).first()
            livros = user.livros
        return render_template('livros.html', livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano = request.form['ano']

        with SessionLocal() as session:
            with session.begin():
                livro = Livro(titulo=titulo, ano=ano, autor_id=current_user.id)
                session.add(livro)
                user = session.query(User).where(User.id == current_user.id).first()
                user.livros.append(livro)

            flash('Livro adicionado com sucesso!', 'success')
            return redirect(url_for('listar_livros'))
    return render_template('livro_form.html', action='Adicionar')


# Atualizar dados básicos de livro

@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    with SessionLocal() as session:
        with session.begin():
            livro = session.query(Livro).where(Livro.id == id).first()
            if request.method == 'POST':
                livro.titulo = request.form['titulo']
                livro.ano = request.form['ano']
                session.add(livro)
                flash('Livro atualizado com sucesso!', 'success')
                return redirect(url_for('listar_livros'))
        return render_template('livro_form.html', action='Editar', livro=livro)


@app.route('/livros/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_livro(id):
    
    with SessionLocal() as session:
        with session.begin():
            livro = session.query(Livro).where(Livro.id == id).first()
            session.delete(livro)
        return redirect(url_for('listar_livros'))


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)