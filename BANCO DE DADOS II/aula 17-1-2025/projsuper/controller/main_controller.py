"""
Kauê Rian Silva - UTF8 - ptbr
main_controller.py
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.mysql_config import db, Cliente
from werkzeug.security import check_password_hash  # Para validar o hash da senha

# Criação de um Blueprint para o controlador principal
main_bp = Blueprint('main', __name__)

# Rota principal (landing)
@main_bp.route('/')
def index():
    return render_template('landing.html')

# Rota para a página inicial (home)
@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not email or not senha:
            flash('Por favor, preencha todos os campos.', 'warning')
            return redirect(url_for('main.entrar'))

        try:
            # Busca o usuário no banco
            user = Cliente.query.filter_by(email=email).first()

            if not user:
                flash('E-mail não cadastrado!', 'danger')
                return redirect(url_for('main.entrar'))

            # Valida o hash da senha
            if not check_password_hash(user.senha, senha):
                flash('Senha incorreta!', 'danger')
                return redirect(url_for('main.entrar'))

            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            flash(f"Erro ao acessar o banco de dados: {e}", 'danger')
            return redirect(url_for('main.entrar'))

    return render_template('entrar.html')

@main_bp.route('/cadastrar')
def cadastrar_usuario():
    return render_template('cadastro.html')

@main_bp.route('/esqueci_senha')
def esqueci_senha():
    return "Página para recuperar senha"

@main_bp.route('/add-user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        try:
            # Cria um hash da senha
            from werkzeug.security import generate_password_hash
            senha_hash = generate_password_hash(senha)

            # Cria o cliente com a senha segura
            novo_cliente = Cliente(nome=nome, email=email, senha=senha_hash)
            db.session.add(novo_cliente)
            db.session.commit()
            flash('Usuário adicionado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar usuário: {e}', 'danger')
            return redirect(url_for('main.index'))
