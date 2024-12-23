"""
Kauê Rian Silva Conceição Oliveira - UTF8 - PTBR
"""

import re

def validar_usuario(usuario, mysql):
    """Validações para o campo usuário"""
    if not usuario or ' ' in usuario:
        return "Usuário não pode ser vazio ou conter espaços."
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuario WHERE Usuario = %s', (usuario,))
    if cursor.fetchone():
        return "Usuário já está em uso."
    return None

def validar_email(email, mysql):
    """Validações para o campo email"""
    if not email or ' ' in email or '@' not in email:
        return "Email inválido."
    email = email.lower()  # Converter para minúsculas
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuario WHERE Email = %s', (email,))
    if cursor.fetchone():
        return "Email já está em uso."
    return None

def validar_senha(senha):
    """Validações para o campo senha"""
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres."
    if not re.search(r'[A-Z]', senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r'[a-z]', senha):
        return "A senha deve conter pelo menos uma letra minúscula."
    if not re.search(r'[0-9]', senha):
        return "A senha deve conter pelo menos um número."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return "A senha deve conter pelo menos um caractere especial."
    return None

def salvar_usuario(usuario, email, senha, mysql):
    """Tenta salvar o usuário no banco de dados"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuario (Usuario, Email, Senha) VALUES (%s, %s, %s)', 
                       (usuario, email.lower(), senha))
        mysql.connection.commit()
        cursor.close()
        return "Usuário cadastrado com sucesso!", None
    except Exception as e:
        return None, "Erro ao salvar no banco de dados."
