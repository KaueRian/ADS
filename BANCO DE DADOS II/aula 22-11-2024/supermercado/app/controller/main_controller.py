"""
Kauê Rian Silva Conceição Oliveira - UTF8 - PTBR
"""

from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import RegistrationForm
from app import mysql

main = Blueprint('main', __name__)

@main.route('/')
def form():
    return render_template('form.html')

@main.route('/login', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        usuario = form.usuario.data
        email = form.email.data
        senha = form.senha.data

        # Insert user into database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO usuario (usuario, email, senha) VALUES (%s, %s, %s)',
            (usuario, email, senha)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('main.form'))

    return render_template('register.html', form=form)
