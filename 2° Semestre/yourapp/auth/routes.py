from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Se o usuário já estiver logado, redireciona
    if current_user.is_authenticated:
        return redirect(url_for('products.list_products'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validações básicas
        if not username or not email or not password:
            flash('Todos os campos são obrigatórios.')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('As senhas não coincidem.')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.')
            return render_template('auth/register.html')
        
        # Verifica se usuário ou email já existem
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe. Escolha outro.')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.')
            return render_template('auth/register.html')
        
        try:
            # Cria novo usuário
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registro realizado com sucesso! Faça login.')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar usuário. Tente novamente.')
            return render_template('auth/register.html')
    
    # GET request - mostra o formulário
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('products.list_products'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        if not username or not password:
            flash('Por favor, preencha todos os campos.')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Redireciona para a página que o usuário tentava acessar ou para produtos
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('products.list_products'))
        else:
            flash('Usuário ou senha inválidos.')
            return render_template('auth/login.html')
    
    # GET request - mostra o formulário
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('auth.login'))