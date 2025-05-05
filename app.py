from flask import Flask, render_template, request, make_response, url_for, redirect

app = Flask(__name__)

preferencias_usuarios = {}

@app.route('/', methods=['GET', 'POST'])
def pag_inicial():
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        ano = request.form.get('ano')
        diretor = request.form.get('diretor')
        
        preferencias_usuarios = {
            'genero': genero,
            'ano': ano,
            'diretor': diretor
        }
        response = make_response(redirect(url_for('ver')))
        response = set.cookie('ultimo_usuario', nome)
        return response

    return render_template('cadastrar.html')

@app.route('/ver')
def ver():
    nome = request.cookies.get('ultima_usuario') or request.args.get('nome')
    
    if nome in preferencias_usuarios:
        preferencias = preferencias_usuarios[nome]
        return render_template('ver.html', nome=nome, preferencias=preferencias)
    else:
        return render_template('ver.html', nome=None)

if __name__ == '__main__':
    app.run(debug=True)
