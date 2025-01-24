"""
Kauê Rian Silva - UTF8 - ptbr
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.mysql_config import db, Cliente  # Importa o SQLAlchemy e o modelo Cliente

# Criação de um Blueprint para o controlador principal
main_bp = Blueprint('main', __name__)

# Rota principal (landing)
@main_bp.route('/')
def index():
    # Exibe a página inicial (landing page).
    return render_template('landing.html')

# Rota para a página inicial (home)
@main_bp.route('/home')
def home():
    # Exibe a página principal (home).
    return render_template('home.html')

@main_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    # Gerencia a página de login.
    # Se for uma requisição POST, valida as credenciais do usuário.
    # Se for GET, exibe o formulário de login.

    if request.method == 'POST':
        # Captura os dados do formulário
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            # Verifica no banco de dados se o usuário existe
            user = Cliente.query.filter_by(email=email).first()

            # Se o usuário não for encontrado
            if not user:
                flash('E-mail não cadastrado!', 'danger')
                return redirect(url_for('main.entrar'))

            # Verifica a senha (idealmente deve ser armazenada como hash no banco)
            if user.senha == senha:
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('main.index'))  # Redireciona para a landing page
            else:
                flash('Senha incorreta!', 'danger')
                return redirect(url_for('main.entrar'))

        except Exception as e:
            flash(f"Erro ao acessar o banco de dados: {e}", 'danger')
            return redirect(url_for('main.entrar'))

    # Se for GET, exibe o formulário de login
    return render_template('entrar.html')

@main_bp.route('/cadastrar')
def cadastrar_usuario():
    # Exibe o formulário de cadastro de novos usuários.
    return render_template('cadastro.html')

@main_bp.route('/esqueci_senha')
def esqueci_senha():
    # Página para recuperação de senha.
    return "Página para recuperar senha"

# Rota para adicionar um usuário ao banco
@main_bp.route('/add-user', methods=['POST'])
def add_user():
    # Adiciona um novo usuário ao banco de dados.
    # Recebe os dados via POST e os insere no banco.
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        try:
            # Cria um novo cliente
            novo_cliente = Cliente(nome=nome, email=email, senha=senha)
            db.session.add(novo_cliente)  # Adiciona o cliente ao banco
            db.session.commit()          # Confirma as alterações
            flash('Usuário adicionado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()  # Desfaz a transação em caso de erro
            flash(f'Erro ao adicionar usuário: {e}', 'danger')
            return redirect(url_for('main.index'))
