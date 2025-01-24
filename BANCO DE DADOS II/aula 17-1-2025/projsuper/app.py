"""
Kauê Rian Silva - UTF8 - ptbr
app.py
"""
from flask import Flask
from model.mysql_config import Config, init_db, db
from controller.main_controller import main_bp

# Configuração inicial
app = Flask(__name__)

# Carrega as configurações do arquivo mysql_config.py
app.config.from_object(Config)

# Inicializa o SQLAlchemy
init_db(app)

# Registro do blueprint principal
app.register_blueprint(main_bp, url_prefix="/")

# Cria as tabelas no banco de dados, caso ainda não existam
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
