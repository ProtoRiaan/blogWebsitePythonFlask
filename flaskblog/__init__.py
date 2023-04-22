

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


  #instantiate the flask instance 
app = Flask(__name__)


  #configurations for the flask app instance
app.config['SECRET_KEY'] = os.environ.get('FLASK_APP_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  #relative path for DB file
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USR')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PWD')





  #insantiate the DB
db = SQLAlchemy(app)

  #instantiating password hashing  
bcrypt = Bcrypt(app)

  #Instantiating login manager
login_manager=LoginManager(app)
login_manager.login_view = 'Login'
login_manager.login_message_category = 'info'

   #Instantiate the mail client
mail = Mail(app)

from flaskblog import views