from django.db import models


class Categoria(models.Model):
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return f'Categoria {str(self.descricao)[0:5]}'


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
