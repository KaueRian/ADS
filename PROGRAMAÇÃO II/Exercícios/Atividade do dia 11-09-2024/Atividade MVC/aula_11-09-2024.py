#Kauê Rian Silva - PT-BR - UTF-8
#aula_11-09-2024.py - 11/09/2024

class Modelo:
    def __init__(self):
        # Corrected the dictionary structure with proper brackets and values
        self.produtos = {
            'ps5': {'id': 1, 'descricao': 'Playstation 5', 'preco': 4420},
            'xboxx': {'id': 2, 'descricao': 'Xbox Series X', 'preco': 4349},
            'switch': {'id': 3, 'descricao': 'Nintendo Switch', 'preco': 2176}
        }


class Controlador:
    def __init__(self):
        # Controlador initialized with the Modelo class
        self.modelo = Modelo()

    # Method to list products for printing
    def listar_produtos(self):
        produtos = self.modelo.produtos.keys()
        print('>>> PRODUTOS >>>')
        for chave in produtos:
            print(f'ID: {self.modelo.produtos[chave]["id"]}')
            print(f'Descrição: {self.modelo.produtos[chave]["descricao"]}')
            print(f'Preço: {self.modelo.produtos[chave]["preco"]}\n')


class Visao:
    def __init__(self):
        # Visao is initialized with the Controlador class
        self.controlador = Controlador()

    # Method to use Controlador to capture product layout and display to client
    def produtos(self):
        self.controlador.listar_produtos()


# Client running the application to see the products
if __name__ == "__main__":
    visao = Visao()
    visao.produtos()
