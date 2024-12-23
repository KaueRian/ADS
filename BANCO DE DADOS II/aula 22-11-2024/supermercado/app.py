"""
Kauê Rian Silva Conceição Oliveira - UTF8 - PTBR
"""

from app import create_app

app = create_app()

app.config['SECRET_KEY'] = 'supersecretkey'

if __name__ == "__main__":
    app.run(host='localhost', port=5000) 