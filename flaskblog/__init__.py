

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


  #instantiate the flask instance 
app = Flask(__name__)


  #configurations for the flask app instance
app.config['SECRET_KEY'] = '65642ab665b75a1abf898a329f9327f4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  #relative path for DB file


  #insantiate the DB
db = SQLAlchemy(app)

  #instantiating password hashing  
bcrypt = Bcrypt(app)

  #Instantiating login manager
login_manager=LoginManager(app)
login_manager.login_view = 'Login'
login_manager.login_message_category = 'info'

from flaskblog import views