from flask import Flask, render_template, request 

app = Flask(__name__)

# URL PATH ("/") | METHOD (GET,POST)

#ROTA
@app.route('/register', methods=['GET']) # a função register é chamada de "view function"
def index(): # a função index é chamada de "view funciont"
    #jinja2
    return render_template('index.html') # renderiza o template index.html

@app.route('/register', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    return f"voce digitou {nome}"
