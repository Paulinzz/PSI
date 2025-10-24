from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('products.list_products'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash ('Nome de usuário já existe.', 'danger')
            return redirect(url_for('register.html'))

        if User.query.filter_by(email=email).first():
            flash ('Email já cadastrado.', 'danger')
            return redirect(url_for('register.html'))
        
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('auth.login'))

    render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('products.list_products'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')       
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('products.list_products'))
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('auth.login'))