{% extends 'base.html' %}

{% block head %}
    <title>Atualizar Produto</title>
{% endblock %}

{% block body %}
    <h3>Atualizar Produto</h3>

    <form action="{{ url_for('editar_produto', id=produto.id) }}" method="POST">
        <div class="mb-3">
            <label for="descricao" class="form-label">Descrição</label>
            <input class="form-control" type="text" name="descricao" id="descricao" value="{{ produto.descricao }}" required autofocus />
        </div>

        <div class="mb-3">
            <label for="preco" class="form-label">Preço</label>
            <input class="form-control" type="text" name="preco" id="preco" value="{{ produto.preco }}" required />
        </div>

        <div class="mb-3">
            <button type="submit" class="btn btn-primary mb-3">Atualizar</button>
        </div>
    </form>
{% endblock %}
