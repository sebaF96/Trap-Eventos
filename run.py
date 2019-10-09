from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message  # Importar para enviar Mail
from flask_login import LoginManager


load_dotenv(override=True)


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.getenv('DB_CONECTION')+'@localhost/final_database'
db = SQLAlchemy(app)

# Configuraciones de mail
app.config['MAIL_HOSTNAME'] = 'localhost'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SENDER'] = 'Trap Eventos <TrapEventos@noreply.com>'

mail = Mail(app)  # Inicializar mail
login_manager = LoginManager(app)
csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')

if __name__ == '__main__':
    from rutas import *
    app.run(debug=True)
