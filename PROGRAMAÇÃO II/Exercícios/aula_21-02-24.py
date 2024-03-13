# Kaue Rian Silva - 28-02-2024
# aula_21-02-24.py


class Animal:
    def __init__(self, tipo, tamanho=None, peso=None, idade=None):
        self.tipo = tipo
        self.tamanho = tamanho
        self.peso = peso
        self.idade = idade

    def comer(self):
        print(f"O {self.tipo} está comendo!")


ele = Animal("grande")
ele.comer()

elefante = Animal("Elefante", 3, 2700, 30)

print(f"\nTipo do animal: {elefante.tipo}")
print(f"Tamanho: {elefante.tamanho} metros de altura")
print(f"Peso: {elefante.peso} quilos")
print(f"Idade: {elefante.idade} anos")
print(f"Ele é da classe {type(elefante)}")


class Lampada:
    def __init__(self, voltagem, cor, tecnologia, luminosidade, status="Desligada"):
        self.voltagem = voltagem
        self.cor = cor
        self.tecnologia = tecnologia
        self.luminosidade = luminosidade
        self.status = status


lampada_sl = Lampada(220, "Branca", "LED", "Alta")
lampada_qt = Lampada(110, "Amarela", "Filamento", "Baixa", "Ligada")
lampada_cz = Lampada(220, "Vermelha", "Fluorescente", "Média")

print("\nLâmpada SL:")
print(f"Voltagem: {lampada_sl.voltagem}")
print(f"Cor: {lampada_sl.cor}")
print(f"Tecnologia: {lampada_sl.tecnologia}")
print(f"Luminosidade: {lampada_sl.luminosidade}")
print(f"Status: {lampada_sl.status}")

print("\nLâmpada QT:")
print(f"Voltagem: {lampada_qt.voltagem}")
print(f"Cor: {lampada_qt.cor}")
print(f"Tecnologia: {lampada_qt.tecnologia}")
print(f"Luminosidade: {lampada_qt.luminosidade}")
print(f"Status: {lampada_qt.status}")

print("\nLâmpada CZ:")
print(f"Voltagem: {lampada_cz.voltagem}")
print(f"Cor: {lampada_cz.cor}")
print(f"Tecnologia: {lampada_cz.tecnologia}")
print(f"Luminosidade: {lampada_cz.luminosidade}")
print(f"Status: {lampada_cz.status}")


class LoginIntranet:
    def __init__(self, email, senha):
        self.__email = email
        self.__senha = senha


usuario = LoginIntranet("teste@gmail.com", "123456")

print(dir(usuario))

print(f"\nO e-mail do usuário é: {usuario._LoginIntranet__email}")
print(f"A senha do usuário é: {usuario._LoginIntranet__senha}")


class LoginIntranetDois:
    def __init__(self, email, senha):
        self.email = email
        self.__senha = senha

    def mostra_email(self):
        print(self.email)

    def mostra_senha(self):
        print(self.__senha)


usuario_dois = LoginIntranetDois("Gnomica@gmail.com", "654321")
usuario_dois.mostra_email()
usuario_dois.mostra_senha()

usuario_tres = LoginIntranetDois("Gnomica@gmail.com", "654321")
usuario_quatro = LoginIntranetDois("Gertrudez@gmail.com", "01010101")
usuario_cinco = LoginIntranetDois("Genoveva@gmail.com", "4503215")
usuario_seis = LoginIntranetDois("Gerimunda@gmail.com", "987654")

usuario_tres.mostra_email()
usuario_quatro.mostra_email()
usuario_cinco.mostra_email()
usuario_seis.mostra_email()


class Produto:
    imposto = 1.08

    def __init__(self, descricao, cor, marca, tela, valor):
        self.descricao = descricao
        self.cor = cor
        self.marca = marca
        self.tela = tela
        self.valor = valor * Produto.imposto

    def mostra_na_tela(self):
        print(self.descricao)
        print(self.cor)
        print(self.marca)
        print(self.tela)
        print(self.valor)


produto_1 = Produto("Notebook Gamer", "Preto", "Dell", "Monitor 15", 13542.25)
produto_2 = Produto("Magic Mouse 2 A1657", "Branco", "Apple", "2,16 X 5,71 cm", 675.00)

produto_1.mostra_na_tela()
print()
produto_2.mostra_na_tela()


class Produto2:
    imposto = 1.12
    contator = 0

    def __init__(self, descricao, cor, marca, tela, valor):
        self.id = Produto2.contator + 1
        self.descricao = descricao
        self.cor = cor
        self.marca = marca
        self.tela = tela
        self.valor = valor * Produto2.imposto
        Produto2.contator = self.id

    def mostra_na_tela(self):
        print(self.id)
        print(self.descricao)
        print(self.cor)
        print(self.marca)
        print(self.tela)
        print(self.valor)


produto_1 = Produto2("Notebook Gamer", "Preto", "Dell", "Monitor 15", 13542.25)
produto_2 = Produto2("Magic Mouse 2 A1657", "Branco", "Apple", "2,16 X 5,71 cm", 675.00)

produto_1.mostra_na_tela()
print()
produto_2.mostra_na_tela()

produto_1.peso = "5kg"
produto_2.peso = "950gr"
produto_1.mostra_na_tela()
print(f"Peso: {produto_1.peso}")
print()
produto_2.mostra_na_tela()
print(f"Peso: {produto_2.peso}")

print("\n", dir(produto_1))
print("\n", dir(produto_2))

del produto_2.peso
del produto_2.tela
print("\n", dir(produto_2))
