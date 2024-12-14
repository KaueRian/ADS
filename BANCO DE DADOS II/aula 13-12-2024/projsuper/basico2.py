from sqlite3 import Cursor
from flask import Flask
from flask_mysqldb import MySQL
from model.mysql_config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

if __name__ == "__main__":
    with app.app_context():  # Cria um contexto de aplicação
        try:
            # Tenta conectar ao banco de dados e executar uma consulta
            print("Conectando ao banco de dados...")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios;")  # Substitua pela sua tabela
            users = cur.fetchall()
            cur.close()
            print(f"Usuários encontrados: {users}")  # Exibe os usuários retornados
        except Exception as e:
            # Captura e exibe qualquer erro ocorrido
            print(f"Erro ao conectar ao banco de dados: {e}")