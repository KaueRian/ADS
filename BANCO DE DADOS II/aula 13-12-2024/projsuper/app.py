"""
Claudinei de Oliveira - UTF8 - ptbr
"""
from flask import Flask, render_template, request, url_for, flash, redirect
from model.mysql_config import Config, init_mysql, mysql
from controller.main_controller import main_bp

# Configuração inicial
app = Flask(__name__)

app.config.from_object(Config)

init_mysql(app)

# Registro do blueprint principal
app.register_blueprint(main_bp)

@app.route('/cadastrar')
def cadastrar_usuario():
    return render_template('cadastro.html')

@app.route('/esqueci_senha')
def esqueci_senha():
    return "Página para recuperar senha"


# Rota para adicionar um usuário (exemplo de interação com o banco)
@app.route('/add-user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
            mysql.connection.commit()
            cur.close()
            flash('Usuário adicionado com sucesso!', 'success')
            return redirect(url_for('test_db'))
        except Exception as e:
            flash(f'Erro ao adicionar usuário: {e}', 'danger')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)