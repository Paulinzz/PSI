from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Dicionário fixo de recomendações por gênero
FILMES_POR_GENERO = {
    'acao': ['Missão Impossível', 'John Wick', 'Mad Max: Estrada da Fúria'],
    'comedia': ['Se Beber, Não Case', 'As Branquelas', 'Debi & Lóide'],
    'drama': ['Cidadão Kane', 'O Poderoso Chefão', 'Forrest Gump'],
    'ficcao': ['Blade Runner 2049', 'Interestelar', 'Matrix'],
    'terror': ['Hereditário', 'O Exorcista', 'Corra!']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        notificacoes = 'Sim' if request.form.get('notificacoes_email') else 'Não'
        
        # Criar resposta de redirecionamento
        response = make_response(redirect(url_for('ver_preferencias')))
        
        # Configurar cookies com validade de 7 dias
        response.set_cookie('nome_usuario', nome, max_age=604800)
        response.set_cookie('genero', genero, max_age=604800)
        response.set_cookie('notificacoes_email', notificacoes, max_age=604800)
        
        return response
    
    return render_template('cadastrar.html')

@app.route('/preferencias')
def ver_preferencias():
    # Recuperar dados dos cookies
    nome = request.cookies.get('nome_usuario')
    genero = request.cookies.get('genero')
    notificacoes = request.cookies.get('notificacoes_email')
    
    if nome:
        return render_template('preferencias.html',
                             nome=nome,
                             genero=genero,
                             notificacoes=notificacoes)
    return render_template('preferencias.html', nome=None)

@app.route('/recomendar')
def recomendar():
    genero = request.args.get('genero', '').lower()
    filmes = FILMES_POR_GENERO.get(genero, [])
    return render_template('recomendar.html', genero=genero, filmes=filmes)

if __name__ == '__main__':
    app.run(debug=True)