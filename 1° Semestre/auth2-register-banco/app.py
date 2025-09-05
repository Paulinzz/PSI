# app.py
import os
import sqlite3
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import (
    LoginManager, 
    login_required,
    login_user, 
    logout_user, 
    current_user
)
from modelos import User

# Configurações
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-secreta-padrao')  # Melhor usar variável de ambiente

# Configuração do Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Gerenciamento de conexão com banco de dados
def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        
        if not email or not senha:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('login'))
        
        user = User.get_by_email(email)
        
        if user and user.verify_password(senha):
            login_user(user)
            return redirect(url_for('dash'))
        
        flash('Email ou senha inválidos.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '').strip()
        
        # Validações
        if not email or not senha or not confirmar_senha:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('register'))
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'error')
            return redirect(url_for('register'))
        
        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'error')
            return redirect(url_for('register'))
        
        # Verificar se usuário já existe
        if User.get_by_email(email):
            flash('Este email já está cadastrado.', 'error')
            return redirect(url_for('register'))
        
        # Criar novo usuário
        new_user = User.create(email, senha)
        if new_user:
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        
        flash('Erro ao criar conta. Tente novamente mais tarde.', 'error')
    
    return render_template('register.html')

@app.route('/dash')
@login_required
def dash():
    return render_template('dashboard.html', 
                           lista_usuarios=User.all(),
                           current_user=current_user)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    user_id = request.form.get('user_id')
    
    if not user_id:
        flash('ID de usuário inválido.', 'error')
        return redirect(url_for('dash'))
    
    if str(current_user.id) == user_id:
        flash('Você não pode excluir sua própria conta.', 'error')
        return redirect(url_for('dash'))
    
    if User.delete(user_id):
        flash('Usuário excluído com sucesso.', 'success')
    else:
        flash('Erro ao excluir usuário.', 'error')
    
    return redirect(url_for('dash'))