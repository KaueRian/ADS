# Kauê Rian Silva Conceição Oliveira UTF-8 PT-BR
# aula_19-03-2024.py  20/03/2024


import datetime


class Animal:
    def __init__(self, nome, especie):
        self.nome = nome
        self._especie = especie

    def som(self, som):
        print(f"O som que o {self.nome} faz chama-se: {som}")


class Elefante(Animal):
    def __init__(self, nome, especie, raca):
        super().__init__(nome, especie)
        self.som("bramido")
        self.raca = raca


class Girafa(Animal):
    def __init__(self, nome, especie, raca):
        super().__init__(nome, especie)
        self._raca = raca


dumbo = Elefante("Dumbo", "Elefante", "Loxodonta africana")
gisela = Girafa("Gisela", "Girafa", "Giraffidae")
gisela.som("Zumbido")


class SuperClasse_1:
    pass


class SuperClasse_2:
    pass


class SuperClasse_3:
    pass


class Multi_Derivada_Direta(SuperClasse_1, SuperClasse_2, SuperClasse_3):
    pass


class SuperClasse_1:
    pass


class SuperClasse_2(SuperClasse_1):
    pass


class SuperClasse_3(SuperClasse_2):
    pass


class Multi_Derivada_Indireta(SuperClasse_3):
    pass


class Animal:
    def __init__(self, nome):
        self.nome = nome

    def cumprimentar(self):
        return f"Eu sou {self.nome}"


class Terrestre(Animal):  # Herança direta
    def __init__(self, nome):
        super().__init__(nome)

    def andar(self):
        return f"Olá eu sou {self.nome} e estou andando pela mata"

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self.nome} e vivo em florestas tropicais!"


class Aquatico(Animal):  # Herança direta
    def __init__(self, nome):
        super().__init__(nome)

    def nadar(self):
        return f"O {self.nome} nada e é um peixe filtrante."

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self.nome} e vivo em agua doce"


tatu = Terrestre("Tatu bola")  # herança direta
print()
print(tatu.andar())
print()
print(tatu.cumprimentar())


peixe = Aquatico("Tambaqui")
print()
print()
print(peixe.nadar())
print()
print(peixe.cumprimentar())


print(f"\nTatu Bola é instância de Tatu?: {isinstance(tatu, Terrestre)}")
print(f"\nTambaqui é instância de peixe?: {isinstance(peixe, Aquatico)}")


class Animal:
    def __init__(self, nome):
        self._nome = nome

    def cumprimentar(self):
        return f"Eu sou {self._nome}"


class Terrestre(Animal):  # Herança direta
    def __init__(self, nome):
        super().__init__(nome)

    def andar(self):
        return f"Olá eu sou {self._nome} e estou andando pela mata"

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self._nome} e vivo em florestas tropicais!"


class Aquatico(Animal):  # Herança direta
    def __init__(self, nome):
        super().__init__(nome)

    def nadar(self):
        return f"O {self._nome} nada e é um peixe filtrante."

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self._nome} e vivo em agua doce"


class Ornitorrinco(Terrestre, Aquatico):  # classe multi deverivada direta
    def __init__(self, nome):
        super().__init__(nome)

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self._nome} e vivo na terra e na agua doce!"


perry = Ornitorrinco("Perry")
print("\n", perry.andar())
print("\n", perry.nadar())
print("\n", perry.cumprimentar())


class Pinguim(Ornitorrinco):  # classe multi deverivada indireta
    def __init__(self, nome):
        super().__init__(nome)

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self._nome} e vivo na terra e na agua salgada!"


pinguim = Pinguim("Picolino")
print()
print(pinguim.nadar())
print()
print(pinguim.cumprimentar())


print()
print(f"Pinguim Picolino é da instância pinguin?: {isinstance(pinguim, Pinguim)}")


pinguim = Pinguim("Picolino")
print()
print(pinguim.nadar())
print()
print(pinguim.cumprimentar())


print()
print(f"Pinguim Picolino é da instância pinguin?: {isinstance(pinguim, Pinguim)}")


class Ornitorrinco(Terrestre, Aquatico):  # classe multi deverivada direta
    def __init__(self, nome):
        super().__init__(nome)

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self._nome} e vivo na terra e na agua doce!"


print()
perry = Ornitorrinco("Perry")
print(perry.cumprimentar())  # Metodo Resolution Order ou MRO


class Ornitorrinco(Terrestre, Aquatico):  # classe multi deverivada direta
    def __init__(self, nome):
        super().__init__(nome)


print()
perry = Ornitorrinco("Perry")
print(perry.cumprimentar())  # Metodo Resolution Order ou MRO


class Ornitorrinco(Aquatico, Terrestre):
    def __init__(self, nome):
        super().__init__(nome)


print()
perry = Ornitorrinco("Perry")
print(perry.cumprimentar())


class Ornitorrinco(Aquatico, Terrestre):  # classe multi deverivada direta
    def __init__(self, nome):
        super().__init__(nome)

    def cumprimentar(self):  # sobrescrição do método da classe super()
        return f"Eu sou {self._nome} e vivo na terra e na agua doce!"


print()
perry = Ornitorrinco("Perry")
print(perry.cumprimentar())  # Metodo Resolution Order ou MRO
print(help(Ornitorrinco))


class Animal(object):
    def __init__(self, nome):
        self.nome = nome

    def emite_som(self):
        raise NotImplementedError("A classe filha precisa implementar esse método")

    def come(self):
        print(f"{self.nome} está comendo")


class Cachorro(Animal):
    def __init__(self, nome):
        super().__init__(nome)

    def emite_som(self):
        print(f"{self.nome} fala wau wau")


class Gato(Animal):
    def __init__(self, nome):
        super().__init__(nome)

    def emite_som(self):
        print(f"{self.nome} fala miau miau")


print()
feliz = Gato("Feliz")
feliz.come()
feliz.emite_som()
print()
gerivaldo = Cachorro("Gerivaldo")
gerivaldo.come()
gerivaldo.emite_som()


class Livros:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas


livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
livro_2 = Livros("Programação Funcional para Leigos", "Jhon Paul Mueller", 481)


print(f"\n Livro: {livro_1}")
print(f"\n Livro: {livro_2}")


class Livros:
    def __init__(self, titulo, autor, paginas):
        self._titulo = titulo
        self.autor = autor
        self._paginas = paginas

    def __repr__(self):
        return f"{self._titulo} escrito por {self._autor} - nº páginas: {self._paginas}"


# - Testando
livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
livro_2 = Livros("Programação Funcional para Leigos", "Jhon Paul Mueller", 481)


class Livros:
    def __init__(self, titulo, autor, paginas):
        self._titulo = titulo
        self._autor = autor
        self._paginas = paginas

    def __str__(self):
        return f"{self._titulo} escrito por {self._autor} - nº páginas: {self._paginas}"


# - Testando
livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
livro_2 = Livros("Programação Funcional para Leigos", "Jhon Paul Mueller", 481)
print(f"\n Livro: {livro_1}")
print(f"\n Livro: {livro_2}")


class Livros:
    def __init__(self, titulo, autor, paginas):
        self._titulo = titulo
        self._autor = autor
        self._paginas = paginas

    def __len__(self):
        return self._paginas


# - Testando
livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
livro_2 = Livros("Programação Funcional para Leigos", "Jhon Paul Mueller", 481)
print(f"\n Livro: {livro_1}")
print(f"\n Livro: {livro_2}")


class Livros:
    def __init__(self, titulo, autor, paginas):
        self._titulo = titulo
        self._autor = autor
        self._paginas = paginas

    def __del__(self):
        print(
            f"{self._titulo} escrito por {self._autor} - nº páginas: {self._paginas} foi deletado"
        )


# - Testando
livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
livro_2 = Livros("Programação Funcional para Leigos", "Jhon Paul Mueller", 481)
print(f"\n Livro: {livro_1}")
print(f"\n Livro: {livro_2}")
del livro_1
del livro_2


class Livros:
    def __init__(self, titulo, autor, paginas):
        self._titulo = titulo
        self._autor = autor
        self._paginas = paginas

    def __add__(self, other):
        return f"{self._titulo} escrito por {self._autor} - nº páginas: {self._paginas + other._paginas}"


# - Testando
livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
livro_2 = Livros("Programação Funcional para Leigos", "Jhon Paul Mueller", 481)
print(f"\n Livro: {livro_1 + livro_2}")


class Livros:
    def __init__(self, titulo, autor, paginas):
        self._titulo = titulo
        self._autor = autor
        self._paginas = paginas

    def __str__(self):
        return self._titulo

    def __mul__(self, numero):
        if isinstance(numero, int):
            mensagem = ""
            for n in range(numero):
                mensagem += "-" + str(self)
            return mensagem
        return "Não foi possível multiplicar"


# - Testando
livro_1 = Livros(
    "Python: Guia Prático do Básico ao Avançado", "Rafael F. V. C. Santos", 225
)
print("\n", livro_1 * 3)


print()
print(dir(datetime))


print(datetime.MAXYEAR)
print(datetime.MINYEAR)


print()
print(datetime.datetime.now())


print(repr(datetime.datetime.now()))


inicio = datetime.datetime.now()
print("Data e hora capturada pela variável início: ", inicio)
print()
inicio = inicio.replace(year=2026, hour=16, minute=0, second=0, microsecond=0)
print("Data e horas alteradas na variável:", inicio)
print()
print("Data e hora atual: ", datetime.datetime.now())


evento = datetime.datetime(2019, 1, 1, 0)
print(evento)
print(type(evento))
print(type("31/12/2018"))
data = input("Informe sua data de nascimento (dd/mm/yyyy): ")
data = data.split("/")
data = datetime.datetime(int(data[2]), int(data[1]), int(data[0]))
print()
print(data)
print(type(data))
