from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from modelos import User
from database import obter_conexao

login_manager = LoginManager() 
app = Flask(__name__)
app.secret_key = 'uma_chave_segura_aqui'  # Altere para uma chave segura
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))

    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']

        user = User.get_by_email(email)
        if user and user.check_password(senha):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dash'))
        else:
            flash('Email ou senha incorretos', 'error')
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']
       
        if User.get_by_email(email):
            flash('Email já cadastrado', 'error')
            return redirect(url_for('register'))
            
        user = User.create(email, senha)
        if user:
            login_user(user)
            flash('Cadastro realizado com sucesso!', 'success')
            return render_template('login.html')
        else:
            flash('Erro ao criar conta', 'error')
    return render_template('register.html')

@app.route('/dash')
@login_required
def dash():
    return render_template('dashboard.html', 
                           current_user=current_user,
                           lista_usuarios=User.get_all())

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash('Você não pode deletar sua própria conta', 'error')
        return redirect(url_for('dash'))
    
    conexao = obter_conexao()
    conexao.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conexao.commit()
    conexao.close()
    
    flash('Usuário deletado com sucesso', 'success')
    return redirect(url_for('dash'))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)