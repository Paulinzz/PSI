from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def soma():
    if request.method == 'POST':
        n1 = int(request.form['n1'])
        n2 = int(request.form['n2'])
        resultado = n1 + n2
        return render_template('index.html', resultado=resultado)
    return render_template('atv1.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    