"""
Kauê Rian Silva Conceição Oliveira - UTF8 - PTBR
"""

from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alunoifro'
app.config['MYSQL_DB'] = 'supermercado'
 
mysql = MySQL(app)
 
@app.route('/')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuario (usuario, email, senha) VALUES(%s,%s,%s)',(usuario,email,senha))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=5000)