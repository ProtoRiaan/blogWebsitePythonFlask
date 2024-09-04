

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

projects_data = [
    {
        "projectID" : "1",
        "projectTitle" : "Test Project One",
        "projectImage" : "projectOneCard.png",
        "projectCardText" : "This is the text of Test Project One Card",
        "projectIntroduction" : " This is the introductory text for Test Project 1",
        "projectSections" : [
            { 
                "sectionID" : "1",
                "sectionImages" : ["s1-image1.png","s1-image2.png","s1-image3.png"],
                "sectionText" : "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. \"What's happened to me?\" he thought. It wasn't a dream. His room, a proper human "
            },
            { 
                "sectionID" : "2",
                "sectionImages" : ["s2-image1.png","s2-image2.png","s2-image3.png"],
                "sectionText" : "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. \"What's happened to me?\" he thought. It wasn't a dream. His room, a proper human "
            },
            
        ]
    },
    {
        "projectID" : "2",
        "projectTitle" : "Test Project Two",
        "projectImage" : "projectTwoCard.png",
        "projectCardText" : "This is the text of Test Project Two Card",
        "projectIntroduction" : " This is the introductory text for Test Project 2",
        "projectSections" : [
            { 
                "sectionID" : "1",
                "sectionImages" : ["s1-image1.png","s1-image2.png","s1-image3.png"],
                "sectionText" : "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. \"What's happened to me?\" he thought. It wasn't a dream. His room, a proper human "
            },
            { 
                "sectionID" : "2",
                "sectionImages" : ["s2-image1.png","s2-image2.png","s2-image3.png"],
                "sectionText" : "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. \"What's happened to me?\" he thought. It wasn't a dream. His room, a proper human "
            },
            
        ]
    }

]
