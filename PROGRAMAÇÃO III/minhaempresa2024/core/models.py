from django.db import models
from stdimage.models import StdImageField

# Create your models here.
class Base(models.Model):
    criado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)  # Corrigido para auto_now
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Cargo(models.Model):
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.descricao

class Funcionario(Base):
    nome = models.CharField(max_length=200)
    bio = models.TextField()
    foto = StdImageField(upload_to='equipe', variations={'thumb': {'width': 500, 'height': 500, 'crop': True}})
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, blank=True, null=True)

    facebook = models.CharField(max_length=150, blank=True, null=True)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    linkedin = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'funcionário'
        verbose_name_plural = 'funcionários'

    def __str__(self):
        return self.nome


class Servicos(Base):
    nome = models.CharField(max_length=200)
    foto = StdImageField(upload_to='serviços', variations={'thumb': {'width': 100, 'height': 100, 'crop': True}})
    descricao = models.TextField()

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'

    def __str__(self):
        return self.nome