


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

  #instantiate the DB
db = SQLAlchemy()
migrate = Migrate()


  #instantiating password hashing  
bcrypt = Bcrypt()

  #Instantiating login manager
login_manager=LoginManager()
login_manager.login_view = 'users.Login'
login_manager.login_message_category = 'info'

   #Instantiate the mail client
mail = Mail()




 #instantiate the flask app instance 
def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)


  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)
  migrate.init_app(app, db)
  
  from flaskblog.users.views import users
  from flaskblog.posts.views import posts
  from flaskblog.main.views import main
  from flaskblog.errors.handlers import errors
  from flaskblog.projects.views import projects
  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(main)
  app.register_blueprint(errors)
  app.register_blueprint(projects)

  return app
