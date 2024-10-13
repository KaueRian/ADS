from flask import Blueprint, render_template, request, redirect, url_for
from models.produto_model import Produto

produto_blueprint = Blueprint('produto', __name__)

@produto_blueprint.route("/")
def index():
    produtos = Produto.get_produtos()
    return render_template('index.html', produtos=produtos)

@produto_blueprint.route("/novo", methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        descricao = request.form.get('descricao', None)
        preco = request.form.get('preco', None)
        produto = Produto(descricao=descricao, preco=preco)
        produto.salvar()
        return redirect(url_for('produto.index'))
    else:
        return render_template('novo.html')

@produto_blueprint.route("/atualiza/<int:id>/<int:status>", methods=['GET'])
def atualiza(id, status):
    produto = Produto.get_produto(id)
    produto.status = status
    produto.atualizar()
    return redirect(url_for('produto.index'))

@produto_blueprint.route("/deleta/<int:id>", methods=['GET'])
def deleta(id):
    produto = Produto.get_produto(id)
    produto.deletar()
    return redirect(url_for('produto.index'))

def init_app(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/produto/novo', 'novo', novo, methods=['GET', 'POST'])
    app.add_url_rule('/produto/atualiza/<int:id>/<int:status>', 'atualiza', atualiza, methods=['GET'])
    app.add_url_rule('/produto/deleta/<int:id>', 'deleta', deleta, methods=['GET'])
