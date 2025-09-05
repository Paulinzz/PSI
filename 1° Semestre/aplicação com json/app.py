from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import json
import os

app = Flask(__name__)
app.secret_key = 'uma_chave_muito_secreta_e_forte_aqui' 

# Caminhos dos arquivos
ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PREFERENCIAS = 'preferencias.json'
ARQUIVO_COMPRAS = 'compras.json'

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Variáveis globais para armazenamento de dados
usuarios = {}
cadastros_registrados = []
compras = {}

# Carrega dados dos arquivos ou inicializa estruturas vazias
def carregar_dados():
    global usuarios, cadastros_registrados, compras
    
    # Carrega usuários
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r') as f:
            usuarios = json.load(f)
    else:
        usuarios = {}
    
    # Carrega preferências
    if os.path.exists(ARQUIVO_PREFERENCIAS):
        with open(ARQUIVO_PREFERENCIAS, 'r') as f:
            cadastros_registrados = json.load(f)
    else:
        cadastros_registrados = []
    
    # Carrega compras
    if os.path.exists(ARQUIVO_COMPRAS):
        with open(ARQUIVO_COMPRAS, 'r') as f:
            compras = json.load(f)
    else:
        compras = {}

def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f)

def salvar_preferencias():
    with open(ARQUIVO_PREFERENCIAS, 'w') as f:
        json.dump(cadastros_registrados, f)

def salvar_compras():
    with open(ARQUIVO_COMPRAS, 'w') as f:
        json.dump(compras, f)

# Inicializa os dados
carregar_dados()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return User(user_id)
    return None

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print("Erro ao renderizar template:", str(e))
        raise

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 

    if request.method == 'POST':
        usuario_digitado = request.form['usuario']
        senha_digitada = request.form['senha']
        senha_hash = usuarios.get(usuario_digitado)

        if senha_hash and check_password_hash(senha_hash, senha_digitada):
            user = User(usuario_digitado)
            login_user(user) 
            flash(f'Bem-vindo, {usuario_digitado}!', 'success') 
            next_page = request.args.get('next') 
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger') 
    return render_template('login.html')

@app.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash('Você foi desconectado.', 'info') 
    return redirect(url_for('index'))

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        novo_usuario = request.form['usuario']
        nova_senha = request.form['senha']

        if novo_usuario in usuarios:
            flash('Nome de usuário já existe. Escolha outro.')
        else:
            usuarios[novo_usuario] = generate_password_hash(nova_senha)
            salvar_usuarios()  # Salva no arquivo
            flash(f'Usuário "{novo_usuario}" cadastrado com sucesso! Faça login agora.', 'success')
            return redirect(url_for('login'))
    return render_template('cadastro_usuario.html')

@app.route('/cadastro_preferencias', methods=['GET', 'POST'])
@login_required
def cadastro_preferencias():
    if request.method == 'GET':
        return render_template('cadastro_preferencias.html')

    nome = request.form['nome']
    genero = request.form['genero']

    cadastros_registrados.append({'nome': nome, 'genero': genero, 'cadastrado_por': current_user.id})
    salvar_preferencias()  # Salva no arquivo
    flash(f'Cadastro de {nome} adicionado com sucesso!', 'success')
    return redirect(url_for('ver_cadastros'))

@app.route('/ver_cadastros')
@login_required
def ver_cadastros():
    # Filtra cadastros apenas do usuário atual
    meus_cadastros = [cadastro for cadastro in cadastros_registrados 
                      if cadastro.get('cadastrado_por') == current_user.id]
    return render_template('ver_cadastros.html', cadastros=meus_cadastros)

@app.route('/remover_cadastro/<string:nome_para_remover>', methods=['POST'])
@login_required 
def remover_cadastro(nome_para_remover):
    global cadastros_registrados
    
    # Remove apenas os cadastros do usuário atual com o nome especificado
    novos_cadastros = []
    removido = False
    for cadastro in cadastros_registrados:
        if cadastro['nome'] == nome_para_remover and cadastro.get('cadastrado_por') == current_user.id:
            removido = True
        else:
            novos_cadastros.append(cadastro)
    
    cadastros_registrados = novos_cadastros
    salvar_preferencias()  # Salva no arquivo
    
    if removido:
        flash(f'Cadastro(s) de "{nome_para_remover}" removido(s) com sucesso!', 'info')
    else:
        flash(f'Nenhum cadastro de "{nome_para_remover}" encontrado para remoção.', 'warning')
    
    return redirect(url_for('ver_cadastros'))

# Rotas para o carrinho de compras
@app.route('/adicionar_carrinho', methods=['POST'])
@login_required
def adicionar_carrinho():
    produto_id = request.form.get('produto_id')
    quantidade = int(request.form.get('quantidade', 1))
    
    if current_user.id not in compras:
        compras[current_user.id] = []
    
    # Verifica se o produto já está no carrinho
    encontrado = False
    for item in compras[current_user.id]:
        if item['produto_id'] == produto_id:
            item['quantidade'] += quantidade
            encontrado = True
            break
    
    if not encontrado:
        compras[current_user.id].append({
            'produto_id': produto_id,
            'quantidade': quantidade
        })
    
    salvar_compras()
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('index'))

@app.route('/finalizar_compra', methods=['POST'])
@login_required
def finalizar_compra():
    if current_user.id in compras and compras[current_user.id]:
        # Limpa o carrinho
        compras[current_user.id] = []
        salvar_compras()
        flash('Compra finalizada com sucesso!', 'success')
    else:
        flash('Seu carrinho está vazio!', 'warning')
    return redirect(url_for('index'))

@app.route('/carrinho')
@login_required
def ver_carrinho():
    carrinho = compras.get(current_user.id, [])
    return render_template('carrinho.html', carrinho=carrinho)

if __name__ == '__main__':
    # Inicializa com dados de teste se os arquivos não existirem
    if not os.path.exists(ARQUIVO_USUARIOS):
        usuarios['testuser'] = generate_password_hash('password123')
        usuarios['admin'] = generate_password_hash('adminpass')
        salvar_usuarios()
    
    if not os.path.exists(ARQUIVO_PREFERENCIAS):
        cadastros_registrados = [
            {'nome': 'Alice', 'genero': 'Drama', 'cadastrado_por': 'testuser'},
            {'nome': 'Bob', 'genero': 'Ação', 'cadastrado_por': 'testuser'},
            {'nome': 'Charlie', 'genero': 'Comédia', 'cadastrado_por': 'admin'},
            {'nome': 'Alice', 'genero': 'Ficção', 'cadastrado_por': 'testuser'}
        ]
        salvar_preferencias()
    
    if not os.path.exists(ARQUIVO_COMPRAS):
        compras = {}
        salvar_compras()
    
    app.run(debug=True)