"""
Claudinei de Oliveira - ptbr
config.py
"""
import os
from flask_mysqldb import MySQL


# Inicializa o aplicativo Flask

class Config:
    # Configuração do MySQL
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")    # Host do banco de dados
    MYSQL_USER = os.getenv("SQL_USER", "root") # Usuário do MySQL
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "alunoifro")    # Senha do MySQL que você utilizou
    MYSQL_DB = os.getenv("MYSQL_DB", "clienteweb") # Nome do seu banco de dados
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))

mysql = MySQL()

def init_mysql(app):
    mysql.init_app(app)