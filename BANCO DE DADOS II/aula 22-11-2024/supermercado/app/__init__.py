from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # App configurations
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'alunoifro'
    app.config['MYSQL_DB'] = 'supermercado'

    # Initialize extensions
    mysql.init_app(app)

    # Register Blueprints
    from app.controller.main_controller import main

    app.register_blueprint(main)

    return app
 