"""
Kauê Rian Silva - UTF8 - ptbr
main_controller.py
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.mysql_config import mysql


# Criação de um Blueprint para o controlador principal
main_bp = Blueprint('main', __name__)

# Rota principal
@main_bp.route('/')
def index():
    return render_template('landing.html')

'''
# Rota para a página de entrada (landing)
@main_bp.route('/landing')
def landing():
    return render_template('landing.html')
'''

# Rota para a página inicial (home)
@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        # Captura os dados do formulário
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            # Verifica o banco de dados para encontrar o usuário
            cur = mysql.connection.cursor()
            cur.execute("SELECT senha FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            # Se o usuário não for encontrado
            if not user:
                flash('E-mail não cadastrado!', 'danger')
                return redirect(url_for('entrar'))

            # Verifica a senha (assumindo que está em texto puro; idealmente use hash)
            if user[0] == senha:
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('index'))  # Redireciona para a página inicial
            else:
                flash('Senha incorreta!', 'danger')
                return redirect(url_for('entrar'))

        except Exception as e:
            flash(f"Erro ao acessar o banco de dados: {e}", 'danger')
            return redirect(url_for('entrar'))

    # Se o método for GET, renderiza a página de login
    return render_template('entrar.html')