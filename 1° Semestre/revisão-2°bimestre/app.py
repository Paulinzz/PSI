from flask import Flask, render_template, request, redirect, url_for, flash
# ^ Ferramentas básicas do Flask para construir o site e mostrar mensagens

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# ^ AS NOVAS FERRAMENTAS DO FLASK-LOGIN PARA SEGURANÇA!
#   - LoginManager: Gerencia tudo sobre login.
#   - UserMixin: Uma ajudinha para criar sua classe de usuário.
#   - login_user: Função para "colocar" o usuário logado na sessão.
#   - logout_user: Função para "tirar" o usuário da sessão.
#   - login_required: Um "guarda" que barra quem não está logado de ver uma página.
#   - current_user: Diz quem é o usuário atualmente logado.

import sqlite3 # Ferramenta para o banco de dados
from iniciar import obter_conexao # Pega a função que te dá a conexão com o banco

app = Flask(__name__) # Cria sua "casa digital" (aplicativo Flask)
app.config['SECRET_KEY'] = 'sua_chave_secreta' # <<< MUITO IMPORTANTE!
# ^ Uma "chave secreta" para proteger as sessões dos usuários. Imagine que é a chave mestra da sua casa.
#   Troque 'sua_chave_secreta' por uma sequência BEM LONGA E ALEATÓRIA na vida real!

login_manager = LoginManager() # Inicia o gerente de login
login_manager.init_app(app) # Conecta o gerente de login à sua casa (aplicativo Flask)
login_manager.login_view = 'login' # Se alguém não logado tentar acessar uma página protegida, será mandado para a página de 'login'

# --- A CLASSE USER (Seu Cartão de Identidade para o Flask-Login) ---
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id # Guarda o ID do usuário
        self.name = name # Guarda o nome do usuário

    @staticmethod
    def get(user_id):
        conn = obter_conexao()
        cursor = conn.execute("SELECT id, nome FROM usuarios WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(user_data[0], user_data[1])
        return None
    # ^ Esta função é como o "porteiro" do Flask-Login. Ele diz:
    #   "Me dê o ID de um usuário, e eu vou buscar os dados dele no banco para ter certeza que ele existe."

    def get_id(self):
        return str(self.id)
    # ^ Esta função é usada pelo Flask-Login para saber qual é o ID único do seu usuário.

# --- CARREGADOR DE USUÁRIO (O Despertador do Flask-Login) ---
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
# ^ Imagine que a cada nova página que um usuário visita, o Flask-Login "esquece" quem ele é.
#   Essa função é como um "despertador": ele usa o ID do usuário (que fica guardado numa "memória temporária" chamada sessão)
#   para "lembrar" quem é o usuário. Ela usa a função `User.get()` que vimos antes.

# --- ROTAS (As Portas da sua Casa Digital) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # Se o usuário JÁ está logado...
        return redirect(url_for('index')) # ...manda ele direto para a página inicial, não precisa logar de novo.

    if request.method == 'POST': # Se o formulário de login foi enviado...
        username = request.form['username'] # Pega o nome de usuário do formulário
        password = request.form['password'] # Pega a senha do formulário

        conn = obter_conexao()
        # AQUI É MUITO IMPORTANTE: Em um aplicativo REAL, você compararia a senha HASHED.
        # Aqui, para simplificar, só verifica se o nome de usuário existe e se a "senha" (que é igual ao nome) bate.
        cursor = conn.execute("SELECT id, nome FROM usuarios WHERE nome = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data: # Se encontrou o usuário no banco de dados...
            if username == password: # E a senha (simulada) bate...
                user = User(user_data[0], user_data[1]) # Cria um objeto User (seu cartão de identidade)
                login_user(user) # <<< FLASK-LOGIN: "Coloca" o usuário na sessão, ele está logado!
                flash('Logado com sucesso!', 'success') # Exibe uma mensagem de sucesso
                return redirect(url_for('index')) # Manda para a página inicial
            else:
                flash('Nome de usuário ou senha inválidos', 'danger') # Mensagem de erro
        else:
            flash('Nome de usuário ou senha inválidos', 'danger') # Mensagem de erro
    return render_template('login.html') # Mostra a página de login (o formulário)

@app.route('/logout')
@login_required # <<< FLASK-LOGIN: Só quem está logado pode acessar esta rota
def logout():
    logout_user() # <<< FLASK-LOGIN: "Tira" o usuário da sessão, ele está desconectado!
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index')) # Manda para a página inicial

@app.route('/', methods=['GET', 'POST'])
@login_required # <<< FLASK-LOGIN: Apenas usuários LOGADOS podem ver esta página!
def index():
    if request.method == 'POST': # Se um formulário foi enviado na página inicial...
        name = request.form['name'] # Pega o nome do formulário

        conn = obter_conexao()
        # Verifica se o nome já existe antes de adicionar
        cursor = conn.execute("SELECT id FROM usuarios WHERE nome = ?", (name,))
        existing_user = cursor.fetchone()
        if not existing_user: # Se o usuário não existe, adiciona
            sql = "INSERT INTO usuarios(nome) VALUES (?)"
            conn.execute(sql, (name,))
            conn.commit()
            flash(f'Usuário {name} adicionado!', 'success')
        else: # Se o usuário já existe, avisa
            flash(f'Usuário {name} já existe!', 'warning')
        conn.close()

        return redirect(url_for('index')) # Recarrega a página para ver a lista atualizada

    # Se a página foi apenas visitada (não um envio de formulário)...
    conn = obter_conexao()
    sql = "SELECT id, nome FROM usuarios" # Busca todos os usuários do banco
    lista_db = conn.execute(sql).fetchall() # Pega os resultados
    conn.close()

    # Converte para um formato mais fácil de usar no HTML
    lista = [{'id': row[0], 'nome': row[1]} for row in lista_db]

    return render_template('index.html', lista=lista) # Mostra a página inicial com a lista

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # Se o usuário JÁ está logado...
        return redirect(url_for('index')) # ...manda ele direto para a página inicial.

    if request.method == 'POST': # Se o formulário de registro foi enviado...
        username = request.form['username']
        password = request.form['password']

        conn = obter_conexao()
        cursor = conn.execute("SELECT id FROM usuarios WHERE nome = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user: # Se o nome de usuário já existe...
            flash('Nome de usuário já existe. Por favor, escolha um diferente.', 'danger')
        else:
            # AQUI É MUITO IMPORTANTE: Em um aplicativo REAL, faça o HASH da senha!
            sql = "INSERT INTO usuarios(nome) VALUES (?)" # Apenas guarda o nome de usuário (e simula senha sendo o nome)
            conn.execute(sql, (username,))
            conn.commit()
            conn.close()
            flash('Registro bem-sucedido! Por favor, faça login.', 'success')
            return redirect(url_for('login')) # Manda para a página de login

    return render_template('register.html') # Mostra a página de registro (o formulário)