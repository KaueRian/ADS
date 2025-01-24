"""
Kauê Rian Silva - ptbr - basico2.py
"""

from flask import Flask
from flask_mysqldb import MySQL
from model.mysql_config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configuração do MySQL
app.config["MYSQL_HOST"] = "localhost"          # Host do banco de dados
app.config["MYSQL_USER"] = "root"              # Usuário do MySQL
app.config["MYSQL_PASSWORD"] = "alunoifro"    # Senha do MySQL que você utilizou
app.config["MYSQL_DB"] = "supermercado"           # Nome do seu banco de dados

mysql = MySQL(app)

if __name__ == "__main__":
    with app.app_context():
        try:
            print("Conectando ao banco de dados...")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuario;")
            users = cur.fetchall()
            cur.close()
            print(f"Usuários encontrados: {users}")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

