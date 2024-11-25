from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from controller.main_controller import validar_usuario, validar_email, validar_senha, salvar_usuario



app = Flask(__name__)
app.secret_key = 'supermercado_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alunoifro'
app.config['MYSQL_DB'] = 'supermercado'

mysql = MySQL(app)

@app.route('/')
def form():
    return render_template('form.html', mensagem=None)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect(url_for('form'))

    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha']

        # Validações
        erro_usuario = validar_usuario(usuario, mysql)
        if erro_usuario:
            return render_template('form.html', mensagem=erro_usuario)

        erro_email = validar_email(email, mysql)
        if erro_email:
            return render_template('form.html', mensagem=erro_email)

        erro_senha = validar_senha(senha)
        if erro_senha:
            return render_template('form.html', mensagem=erro_senha)

        # Salvar usuário no banco
        mensagem_sucesso, mensagem_erro = salvar_usuario(usuario, email, senha, mysql)
        if mensagem_erro:
            return render_template('form.html', mensagem=mensagem_erro)
        return render_template('form.html', mensagem=mensagem_sucesso)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
