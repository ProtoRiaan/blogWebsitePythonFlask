

import jwt
from datetime import datetime, timedelta 
from flaskblog import db, login_manager
from flask_login import UserMixin
from flask import current_app




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


  #creating DB modules
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Posts', backref='author',lazy=True)

    def GenerateToken(self, expiration=1800):
        resetToken = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.utcnow()
                       + timedelta(seconds=expiration)
            },
            current_app.config['RESET_SECRET_KEY'],
            algorithm="HS256"
        )
        return resetToken
    
    def ConfirmToken(token):
        try:
            tokenData = jwt.decode(
                token,
                current_app.config['RESET_SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )
            userID = tokenData.get('confirm')
        except:
            return False
        return User.query.get(userID)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Posts('{self.title}','{self.date_posted}')"

certs = [
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
                "baseFileName" : "default"
            },
            {
                "name" : "DevNet",
                "baseFileName" : "default"
            },
            {
                "name" : "Security_Core",
                "baseFileName" : "default"
            }

        ]
    },
    {
        "vendor" : "Udemy",
        "certs" : [
            {
                "name" : "SQL",
                "baseFileName" : "default"
            },
            {
                "name" : "Prometheus",
                "baseFileName" : "default"
            },
            {
                "name" : "Wire_Shark",
                "baseFileName" : "default"
            }

        ]
    },
    {
        "vendor" : "Other",
        "certs" : [
            {
                "name" : "Nutanix",
                "baseFileName" : "default"
            }
        ]
    }
]
