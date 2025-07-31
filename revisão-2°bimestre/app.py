from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from iniciar import obter_conexao


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        name = request.form['name']
    
        conn = obter_conexao()
        sql = "INSERT INTO usuarios(nome) VALUES (?)"
        conn.execute(sql, (name,))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn = obter_conexao()
    sql = "SELECT * FROM usuarios"
    lista = conn.execute(sql).fetchall()
    conn.close()
        
    return render_template('index.html', lista=lista)
