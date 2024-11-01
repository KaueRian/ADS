from tkinter.font import names

from django.urls import path
from core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),

    # Categoria:

    path('add/categoria', views.CategoriaCreateView.as_view(),
         name='addCategoria'),
    path('listar/categorias', views.CategoriaListView.as_view(),
         name='listarCategorias'),
    path('atualizar/categoria/<int:pk>', views.CategoriaUpdateView.as_view(), name='atualizarCategoria'),
    path('excluir/categoria/<int:pk>', views.CategoriaDeleteView.as_view(), name='excluirCategoria'),

    # Produto:

    path('add/produto', views.ProdutoCreateView.as_view(),
         name='addProduto'),
    path('listar/produto', views.ProdutoListView.as_view(),
         name='listarProdutos'),
    path('atualizar/produto/<int:pk>', views.ProdutoUpdateView.as_view(), name='atualizarProduto'),
    path('excluir/produto/<int:pk>', views.ProdutoDeleteView.as_view(), name='excluirProduto'),

]
