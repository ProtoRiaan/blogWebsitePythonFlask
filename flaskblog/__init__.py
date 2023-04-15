

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


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

from flaskblog import views