from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from database import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=1)

    def __init__(self, descricao, preco, id=None):
        self.id = id
        self.descricao = descricao
        self.preco = preco

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def atualizar(self):
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_produtos():
        return Produto.query.all()

    @staticmethod
    def get_produto(id):
        return Produto.query.get(id)
