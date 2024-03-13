# Kaue Rian Silva - 28-02-2024
# aula_28-02-2024.py

import os
import platform
from passlib.hash import pbkdf2_sha512 as cryptografa

root_dir = os.getcwd()
print(f"\no Path é: {root_dir} \n")

os.mkdir("clientes")
os.mkdir("produtos")

print(f'\nOs paths e arquivos são: {os.listdir(".")} \n')

root_dir = os.getcwd()
print(f"Diretório inicial do projeto: {root_dir} \n")


def directory_list(radix):
    for radix, directories, _ in os.walk(radix):
        if "venv" in directories:
            directories.remove("venv")
        for directory in directories:
            print(f"Diretórios do projeto: {os.path.join(radix, directory)}")


directory_list(root_dir)


def build_tree(root_dir, prefix="", skip_dirs=None):
    if skip_dirs is None:
        skip_dirs = ["env", "venv"]
    files = sorted(os.listdir(root_dir))
    files_dirs = [
        f
        for f in files
        if os.path.isdir(os.path.join(root_dir, f)) and f not in skip_dirs
    ]

    for i, filename in enumerate(files_dirs):
        path = os.path.join(root_dir, filename)
        is_last = i == (len(files_dirs) - 1)
        print(f"{prefix}{'└──' if is_last else '├──'} {filename}")
        # Se não for o último item, adicione uma linha vertical abaixo deste diretório
        extension = "    " if is_last else "│   "
        build_tree(path, prefix + extension, skip_dirs)


# Obtém o diretório de trabalho atual e inicia a construção da árvore a partir dele
root_dir = os.getcwd()
print(f"Diretório inicial do projeto: {root_dir}")
build_tree(root_dir)

# Verifica se a pasta "clientes" existe no diretório atual
if "clientes" in os.listdir():
    os.chdir("clientes")
    print(f"O path é: {os.getcwd()}\n")
else:
    print("A pasta 'clientes' não foi encontrada no diretório atual.")

os.chdir("..")
print(f"\nO path é: {os.getcwd()}\n")

try:
    os.rename("clientes", "cli")
    print(f'\nO novo nome é: {os.listdir(".")}\n')
except FileNotFoundError:
    print("O diretório ou arquivo 'clientes' não foi encontrado.")

os.rmdir("cli")
print(os.listdir("."))

base_dir = "proj001"
test_dir = os.path.join(base_dir, "teste")
test_client_dir = os.path.join(test_dir, "test_client")
# Cria as diretórios, se eles não existirem
os.makedirs(test_client_dir, exist_ok=True)


# Função para listar estrutura de diretórias de forma recursiva
def build_tree(root_dir, prefix=""):
    items = os.listdir(root_dir)
    items.sort()
    # Ordena arquivos e diretórios
    for i, item in enumerate(items):
        path = os.path.join(root_dir, item)
        is_last = i == (len(items) - 1)
        # Checa se é um diretório e imprime de acordo
        if os.path.isdir(path):
            print(f"{prefix}{'└──' if is_last else '├──'} {item}")
            new_prefix = prefix + ("    " if is_last else "│   ")
            build_tree(path, new_prefix)
        else:
            # Para arquivos
            print(f"{prefix}{'└──' if is_last else '├──'} {item}")


# Imprime estrutura a partir do diretório base
print(f"Estrutura de diretórios a partir de {base_dir}:")
build_tree(base_dir)

base_path = os.path.join("Users", "Edados 2823", "proj 22_11", "teste", "test_client")
# Verifica sistema operacional e ajusta se necessário
if os.name == "nt":  # Sistema operacional Windows
    path_to_remove = os.path.join("C:\\", base_path)  # Ajusta o caminho para o Windows
else:
    path_to_remove = os.path.join("/", base_path)  # Ajusta o caminho para sistemas Unix

try:
    os.rmdir(path_to_remove)
    print(f"O diretório {path_to_remove} foi removido com sucesso.")
except OSError as error:
    print(f"Erro ao remover o diretório {path_to_remove}: {error}")

for subdiretorio in os.listdir("."):
    if os.path.isdir(subdiretorio):
        print(subdiretorio)

if os.path.exists("cli"):
    print("O diretório existe")
else:
    print("O diretório não existe")

# Imprime o nome do sistema
print(platform.system())
# Imprime informações adicionais
print(platform.release())

print("\n", dir())


class Lampada:
    def __init__(self, cor, voltagem, luminosidade):
        self.cor = cor
        self._voltagem = voltagem
        self.luminosidade = luminosidade
        self.ligada = False


class ContaCorrente:
    contador = 6999

    def __init__(self, limite, saldo):
        self.numero = ContaCorrente.contador + 1
        self.limite = limite
        self.saldo = saldo
        ContaCorrente.contador = self.numero


class Produto:
    contador = 0

    def __init__(self, nome, descricao, valor):
        self.id = Produto.contador + 1
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
        Produto.contador = self.id


class Usuario:
    controle = 0

    @classmethod
    def qtd_usuario(cls):
        print(f"\nTotal de usuários cadastrados no sistema: {cls.controle}")

    def __init__(self, nome, sobrenome, email, senha):
        self.id = Usuario.controle + 1
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self._senha = cryptografa.hash(senha, salt_size=32, rounds=12000)
        Usuario.controle = self.id


usuario_um = Usuario("Gnomica", "Cristófina", "Gnomica@gmail.com", "654321")
usuario_um.qtd_usuario()

usuario_dois = Usuario("Gertrudez", "Sanoré", "Gertrudez@gmail.com", "01010101")
