
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

#configurations for the flask app instance
class Config:
    SECRET_KEY = os.environ.get('FLASK_APP_KEY')
    RESET_SECRET_KEY = os.environ.get('FLASK_RESET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  #relative path for DB file
    SERVER_NAME = os.environ.get('FLASK_SERVER_NAME')
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USR')
    MAIL_PASSWORD = os.environ.get('EMAIL_PWD')

    OAUTH2_PROVIDERS = {
        # Google OAuth 2.0 documentation:
        # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
        'google': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'token_url': 'https://accounts.google.com/o/oauth2/token',
            'userinfo': {
                'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
                'email': lambda json: json['email'],
            },
            'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
        },

        # GitHub OAuth 2.0 documentation:
        # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
        'github': {
            'client_id': os.environ.get('GITHUB_CLIENT_ID'),
            'client_secret': os.environ.get('GITHUB_CLIENT_SECRET'),
            'authorize_url': 'https://github.com/login/oauth/authorize',
            'token_url': 'https://github.com/login/oauth/access_token',
            'userinfo': {
                'url': 'https://api.github.com/user/emails',
                'email': lambda json: json[0]['email'],
            },
            'scopes': ['user:email'],
        },
    }

    CERTS = [
    {
        "vendor" : "Comp TIA",
        "certs" : [
            {
                "name" : "Security_Plus",
                "baseFileName" : "secPlus"
            },
            {
                "name" :"A_Plus",
                "baseFileName" : "aPlus"
            }

        ]
    },
    {
        "vendor" : "Cisco",
        "certs" : [
            {
                "name" : "CCNA",
                "baseFileName" : "ccna"
            },
            {
                "name" : "DevNet",
                "baseFileName" : "devnet"
            }
        ]
    },
    {
        "vendor" : "Udemy",
        "certs" : [
            {
                "name" : "SQL",
                "baseFileName" : "udemySQL"
            },
            {
                "name" : "udemyProm",
                "baseFileName" : "udemyProm"
            }
        ]
    },
    {
        "vendor" : "Other",
        "certs" : [
            {
                "name" : "nutanix",
                "baseFileName" : "nutanix"
            }
        ]
    }
]
