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
                    flash('Email já está em uso.', 'warning')
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
        # Carrega o usuário com seus livros
        user = session.query(User).filter(User.id == current_user.id).first()
        
        # Cria uma lista de dicionários para passar ao template (evita objetos desanexados)
        livros_data = []
        for livro in user.livros:
            # Lista os emails dos autores
            autores_emails = [autor.email for autor in livro.autores]
            livros_data.append({
                'id': livro.id,
                'titulo': livro.titulo,
                'ano': livro.ano,
                'autores': ', '.join(autores_emails) if autores_emails else 'Sem autores'
            })
        
    return render_template('livros.html', livros=livros_data)


@app.route('/livros/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        ano = request.form['ano'].strip()
        
        # Obtém os IDs dos autores selecionados
        autores_ids = request.form.getlist('autores')

        with SessionLocal() as session:
            with session.begin():
                # Cria o novo livro
                livro = Livro(titulo=titulo, ano=int(ano) if ano else None)
                
                # Adiciona os autores selecionados ao livro
                for autor_id in autores_ids:
                    autor = session.query(User).filter(User.id == int(autor_id)).first()
                    if autor:
                        livro.autores.append(autor)
                
                # Se nenhum autor foi selecionado, adiciona o usuário atual
                if not autores_ids:
                    user = session.query(User).filter(User.id == current_user.id).first()
                    livro.autores.append(user)
                
                session.add(livro)

            flash('Livro adicionado com sucesso!', 'success')
            return redirect(url_for('listar_livros'))
    
    # GET - busca todos os usuários para selecionar como autores
    with SessionLocal() as session:
        usuarios = session.query(User).all()
        usuarios_data = [{'id': u.id, 'email': u.email} for u in usuarios]
        
    return render_template('livro_form.html', action='Adicionar', usuarios=usuarios_data)


@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    with SessionLocal() as session:
        livro = session.query(Livro).filter(Livro.id == id).first()
        
        if not livro:
            flash('Livro não encontrado.', 'danger')
            return redirect(url_for('listar_livros'))
        
        if request.method == 'POST':
            with session.begin():
                # Atualiza dados básicos do livro
                livro.titulo = request.form['titulo'].strip()
                ano_form = request.form['ano'].strip()
                livro.ano = int(ano_form) if ano_form else None
                
                # Atualiza os autores
                autores_ids = request.form.getlist('autores')
                
                # Limpa os autores atuais
                livro.autores.clear()
                
                # Adiciona os novos autores
                for autor_id in autores_ids:
                    autor = session.query(User).filter(User.id == int(autor_id)).first()
                    if autor:
                        livro.autores.append(autor)
                
                session.add(livro)
            
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('listar_livros'))
        
        # GET - prepara dados para o formulário
        livro_data = {
            'id': livro.id,
            'titulo': livro.titulo,
            'ano': livro.ano,
            'autores_ids': [autor.id for autor in livro.autores]
        }
        
        # Busca todos os usuários
        usuarios = session.query(User).all()
        usuarios_data = [{'id': u.id, 'email': u.email} for u in usuarios]
        
        return render_template('livro_form.html', 
                             action='Editar', 
                             livro=livro_data, 
                             usuarios=usuarios_data)


@app.route('/livros/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_livro(id):
    with SessionLocal() as session:
        with session.begin():
            livro = session.query(Livro).filter(Livro.id == id).first()
            
            if livro:
                session.delete(livro)
                flash('Livro excluído com sucesso!', 'success')
            else:
                flash('Livro não encontrado.', 'danger')
    
    return redirect(url_for('listar_livros'))


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)