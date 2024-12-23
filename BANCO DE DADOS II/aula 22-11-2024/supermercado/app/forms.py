from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from app import mysql

class RegistrationForm(FlaskForm):
    usuario = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters."),
            Regexp(r'^\S+$', message="Username cannot contain spaces.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Length(max=50, message="Email must be less than 50 characters."),
        ]
    )
    senha = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters."),
        ]
    )
    submit = SubmitField('Register')

    def validate_usuario(self, usuario):
        # Check if username is unique
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE usuario = %s", (usuario.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError("This username is already taken. Please choose another.")

    def validate_email(self, email):
        # Check if email is unique
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email.data,))
        email_entry = cursor.fetchone()
        cursor.close()
        if email_entry:
            raise ValidationError("This email is already registered. Please use another.")
