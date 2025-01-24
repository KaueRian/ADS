"""
Kauê Rian Silva - UTF8 - ptbr - mysql_config.py
"""

from flask_sqlalchemy import SQLAlchemy
import os

# Configuração do aplicativo e do banco de dados
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:alunoifro@localhost/supermercado"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))

# Objeto SQLAlchemy
db = SQLAlchemy()

# Inicializa o SQLAlchemy com as configurações do app Flask
def init_db(app):
    db.init_app(app)

# Definição das tabelas e seus relacionamentos
class Cliente(db.Model):
    __tablename__ = "clientes"
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(15))
    pedidos = db.relationship("Pedido", back_populates="cliente")


class Funcionario(db.Model):
    __tablename__ = "funcionarios"
    id_funcionario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    id_cargo = db.Column(db.Integer, db.ForeignKey("cargos.id_cargo"), nullable=False)
    cargo = db.relationship("Cargo", back_populates="funcionarios")


class Cargo(db.Model):
    __tablename__ = "cargos"
    id_cargo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    funcionarios = db.relationship("Funcionario", back_populates="cargo")


class Produto(db.Model):
    __tablename__ = "produtos"
    id_produto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    cliente = db.relationship("Cliente", back_populates="pedidos")
    itens = db.relationship("ItemPedido", back_populates="pedido")


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"
    id_item = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id_pedido"), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id_produto"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto")


class Pagamento(db.Model):
    __tablename__ = "pagamentos"
    id_pagamento = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id_pedido"), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_pagamento = db.Column(db.DateTime, nullable=False)
    pedido = db.relationship("Pedido")
