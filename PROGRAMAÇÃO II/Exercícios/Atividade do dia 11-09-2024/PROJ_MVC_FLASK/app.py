from flask import Flask, render_template, request, redirect, url_for, flash
from models.produto_model import Produto
from sqlalchemy import create_engine, inspect
from database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/rian/Documents/IFRO/programação ii/Atividade do dia 11-09-2024/ifro2023.db'
    app.secret_key = 'seu segredo'
    db.init_app(app)
    return app

def create_tables(app):
    with app.app_context():
        engine = create_engine('sqlite:////home/rian/Documents/IFRO/programação ii/Atividade do dia 11-09-2024/ifro2023.db', echo=True)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if 'produto' not in tables:
            db.create_all()
            print('Tabelas criadas com sucesso!')
        else:
            print('As tabelas já existem.')

app = create_app()

@app.route('/')
def index():
    produtos = Produto.get_produtos()
    return render_template('novo.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        descricao = request.form.get('descricao', None)
        preco = request.form.get('preco', None)
        try:
            preco = float(preco)
        except ValueError:
            flash('O preço deve ser um número válido.')
            produtos = Produto.get_produtos()
            return render_template('novo.html', produtos=produtos)

        produto = Produto(descricao=descricao, preco=preco)
        produto.salvar()
        produtos = Produto.get_produtos()
        return render_template('novo.html', produtos=produtos)

    return render_template('novo.html')

@app.route('/produto/editar/<float:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.get_produto(id)
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        try:
            preco = float(preco)
        except ValueError:
            flash('O preço deve ser um número válido.')
            return render_template('atualizar.html', produto=produto)

        produto.descricao = descricao
        produto.preco = preco
        produto.atualizar()
        return redirect(url_for('index'))

    return render_template('atualizar.html', produto=produto)

@app.route('/produto/atualizar/<int:id>/<int:status>', methods=['GET', 'POST'])
def atualizar_produto(id, status):
    produto = Produto.get_produto(id)
    produto.status = status
    produto.atualizar()
    return redirect(url_for('index'))

@app.route('/produto/deletar/<int:id>', methods=['GET'])
def deletar_produto(id):
    produto = Produto.get_produto(id)
    produto.deletar()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables(app)
    app.run(debug=True)
