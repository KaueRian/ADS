# Kaue Rian Silva - 13-03-2024
# aula_13-03-2024.py

import time


class Televisao:
    def __init__(
        self,
        marca,
        modelo,
        tamanho_tela,
        tipo_tecnologia,
        voltagem,
        nr_serie,
        cod_barras,
        preco,
    ):
        self.marca = marca
        self.modelo = modelo
        self.tamanho_tela = tamanho_tela
        self.tipo_tecnologia = tipo_tecnologia
        self.voltagem = voltagem
        self.nr_serie = nr_serie
        self.codigo_barras = cod_barras
        self.preco = preco
        self.ligada = False
        self.conectada = False
        self.canais = 1

    def verifica_tv_ligada(self):
        return self.ligada

    def ligar_desligar(self):
        if self.ligada:
            self.ligada = False  # se tiver ligada = desliga a tv
        else:
            self.ligada = True  # se tiver desligada liga a tv

    def verifica_conexao(self):
        return self.conectada

    def conecta_tv(self):
        if self.conectada:
            self.conectada = False  # se estiver desconectada irá conectar
        else:
            self.conectada = True  # se estiver desconectda = irá conectar


print()
print(">>> Dados da Televisão <<<<")
print()
marca = input("Marca: ")
modelo = input("Modelo: ")
tamanho_tela = input("Tamanho da tela em polegadas: ")
tipo_tecnologia = input("Tipo de tecnologia: ")
voltagem = input("Voltagem: ")
nr_serie = input("Numero de série: ")
cod_barras = input("Código de Barras: ")
preco = input("Preço de venda R$: ")

tv_1 = Televisao(
    marca, modelo, tamanho_tela, tipo_tecnologia, voltagem, nr_serie, cod_barras, preco
)

print()
print(
    f"A TV: {tv_1.marca}-{tv_1.tipo_tecnologia} - modelo: {tv_1.modelo} - está ligada? {tv_1.verifica_tv_ligada()}"
)
print()
print("Aguarde enquanto sua TV está sendo ligada!!!")
time.sleep(1)
tv_1.ligar_desligar()
print()
print(" - Utilizando sua Televisão -")
print()
print(
    f">>> Bem vindo a sua televisão: {tv_1.marca}-{tv_1.tipo_tecnologia} - modelo: {tv_1.modelo} <<<"
)
print()
print(f" - Você está no menu principal do cliente - canal: {tv_1.canais}")
print()
print(
    input(
        ">>> Escolha uma opção para aproveitar todos os recursos de nossa tecnologia <<<"
    )
)
print()


# 41-Classe lâmpada
class Lampada:
    def __init__(self, cor, voltagem, luminosidade):
        self.cor = cor
        self._voltagem = voltagem
        self.luminosidade = luminosidade
        self.ligada = False

    # Métodos ou ações que o objeto pode realizar
    def checa_lampada(self):
        return self.ligada

    def ligar_desligar(self):
        if self.ligada:
            self._ligada = False
        else:
            self._ligada = True


lampada_1 = Lampada("amarela", 220, 1200)
# executando um método do objeto lampada_1
print(f"A lampada está ligada? {lampada_1.checa_lampada()}")
# Executando outro método do objeto lampada_1
lampada_1.ligar_desligar()
print(f"A lampada está ligada? {lampada_1.checa_lampada()}")


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self._cpf = cpf


class ContaCorrente:
    contador = 4999

    def __init__(self, limite, saldo, cliente):
        self.numero = ContaCorrente.contador + 1
        self.limite = limite
        self.saldo = saldo
        self.cliente = cliente
        ContaCorrente.contador = self.numero

    def mostra_cliente(self):
        print(f"O cliente é: {self.cliente.nome}")

    def mostra_saldo(self):
        print(
            f"O cliente é: {self.cliente.nome} possui um saldo total (saldo + limite) de: {self.saldo + self.limite}"
        )


# 12 - instanciando o Objeto cliente
cliente_1 = Cliente("Gertrudez Gnomica", "145.738.444-89")
# 13-instanciando o Objeto conta
conta = ContaCorrente(2565, 4500, cliente_1)
# 14-executando um método dos objetos conta e cliente_1
conta.mostra_cliente()
# 15-executando outro método dos objetos conta e cliente_1
conta.mostra_saldo()


class Conta:
    contador = 700

    def __init__(self, titular, saldo, limite):
        self.numero = Conta.contador
        self.titular = titular
        self.saldo = saldo
        self.limite = limite
        Conta.contador += 1

    def extrato(self):
        print(
            f"Saldo de {self.saldo} do titular {self.titular}, com limite de {self.limite}"
        )

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
        else:
            print("O valor precisa ser positivo")

    def sacar(self, valor):
        if valor > 0:
            if self.saldo >= valor:
                self.saldo -= valor
            else:
                print("Saldo insuficiente")
        else:
            print("O valor deve ser positivo")

    def transferir(self, valor, conta_destino):
        if self.saldo >= valor:  # remove valor da conta
            self.saldo -= valor
            conta_destino.saldo += valor  # adiciona valor na conta destino
        else:
            print("Saldo insuficiente para transferência")


conta_1 = Conta("Getrudez Gnomica", 100, 500)
conta_2 = Conta("Gastronildo Soares", 1000, 450)
conta_1.extrato()
conta_2.extrato()
print("Transferindo 100 reais da conta 2 para a conta 1 - o novo saldo das contas são:")
conta_2.transferir(100, conta_1)
conta_1.extrato()
conta_2.extrato()
print("Tentando sacar R$ 1.500,00 da conta 1: Gertrudez")
conta_1.sacar(1500)


class Clientes:
    def __init__(self, nome, sobrenome, cpf, renda):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.renda = renda


class Funcionarios:
    def __init__(self, nome, sobrenome, cpf, matricula):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.matricula = matricula

    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"


cliente_1 = Clientes("Genoveva", "Gnomica", "999.888.777-66", 2000)
funcionario_1 = Funcionarios("Festronildo", "Gerundio", "555.4444.333-22", 430125)
print(f"Cliente: {cliente_1.nome_completo()}")
print(f"Funcionário: {funcionario_1.nome_completo()}")


class Pessoas:
    def __init__(self, nome, sobrenome, cpf):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf

    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"


class Clientes(Pessoas):  # Clientes herda da classe pessoas
    def __init__(self, nome, sobrenome, cpf, renda):
        super().__init__(nome, sobrenome, cpf)  # acessa a classe pai
        self.renda = renda


class Funcionarios(Pessoas):  # Funcionarios herda da classe pessoas
    def __init__(self, nome, sobrenome, cpf, matricula):
        super().__init__(nome, sobrenome, cpf)  # acessa a classe pai
        self.matricula = matricula


cliente_1 = Clientes("Genoveva", "Gnomica", "999.888.777-66", 2000)
funcionario_1 = Funcionarios("Festronildo", "Gerundio", "555.4444.333-22", 430125)
print(f"Cliente: {cliente_1.nome_completo()}")
print("Funcionário:", funcionario_1.nome_completo(), "\n")


class Conta:
    contador = 0

    def __init__(self, titular, saldo, limite):
        self.numero = Conta.contador + 1
        self.titular = titular
        self.saldo = saldo
        self.limite = limite
        Conta.contador += 1

    def extrato(self):
        return self.saldo

    def deposita(self, valor):
        self.saldo += valor

    def saca(self, valor):
        self.saldo -= valor

    def transfere(self, valor, destino):
        self.saldo -= valor
        destino.saldo += valor


conta_1 = Conta("Festronildo", 4780.15, 200.35)
conta_2 = Conta("Gertrudez", 3852.35, 308.15)
print(f"\nSaldo da conta_1: {conta_1.extrato()}")
print(f"Saldo da conta_2: {conta_2.extrato()}")
soma = conta_1.get_saldo() + conta_2.get_saldo()
print("-")
print(f"A soma dos saldos é: {soma}")


class Conta:
    contador = 0

    def __init__(self, titular, saldo, limite):
        self._numero = Conta.contador + 1
        self._titular = titular
        self._saldo = saldo
        self._limite = limite
        Conta.contador += 1

    @property
    def numero(self):
        return self._numero

    @property
    def titular(self):
        return self._titular

    @property
    def saldo(self):
        return self._saldo

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, novo_limite):
        self._limite = novo_limite

    def extrato(self):
        return f"\nCliente: {self._titular} - Saldo: {self._saldo}"

    def deposita(self, valor):
        self._saldo += valor

    def saca(self, valor):
        self._saldo -= valor

    def transfere(self, valor, destino):
        self._saldo -= valor
        destino._saldo += valor

    @property
    def valor_total(self):
        return self._saldo + self._limite


conta_1 = Conta("Festronildo", 4780.15, 200.35)
conta_2 = Conta("Gertrudez", 3852.35, 308.15)
print(f"\nSaldo da conta_1: {conta_1.extrato()}")
print(f"Saldo da conta_2: {conta_2.extrato()}")
soma = conta_1.saldo + conta_2.saldo
print(f"\nSoma saldos das contas: {soma}")
print(f"\nO limite da conta_1 é: {conta_1.limite}")
conta_2.limite = 500.00
print(f"\nNovo limite da conta_2 é: {conta_2.limite}")
print(f"\nO Saldo + limite da conta_1 é: {conta_1.valor_total}")
print(f"\nO Saldo + limite da conta_2 é: {conta_2.valor_total}")
