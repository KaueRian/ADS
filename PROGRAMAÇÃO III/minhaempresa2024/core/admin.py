from django.contrib import admin
from core.models import Cargo, Funcionario, Servicos


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'ativo', 'facebook')


@admin.register(Servicos)
class ServicosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')