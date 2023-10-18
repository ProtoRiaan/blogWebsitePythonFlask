
import os

#configurations for the flask app instance
class Config:
    SECRET_KEY = os.environ.get('FLASK_APP_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  #relative path for DB file
    SERVER_NAME = os.environ.get('FLASK_SERVER_NAME')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USR')
    MAIL_PASSWORD = os.environ.get('EMAIL_PWD')
