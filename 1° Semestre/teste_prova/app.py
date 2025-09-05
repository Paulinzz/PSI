
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secreta'

usuarios = {}  # Simulação de banco

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
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = usuarios.get(nome)
        if user and check_password_hash(user['senha'], senha):
            session['usuario'] = nome
            session['carrinho'] = []
            resp = make_response(redirect(url_for('loja')))
            resp.set_cookie('nome', nome)
            return resp
        flash('Login inválido!', 'danger')
    return render_template('login.html')

@app.route('/loja')
def loja():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('loja.html')

@app.route('/adicionar/<item>')
def adicionar(item):
    if 'usuario' in session:
        session['carrinho'].append(item)
        flash(f'{item} adicionado ao carrinho.', 'success')
    return redirect(url_for('carrinho'))

@app.route('/carrinho')
def carrinho():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('carrinho.html', itens=session.get('carrinho', []))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('carrinho', None)
    flash('Logout realizado!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
