

from flask import url_for
from flaskblog import mail
from flask_mail import Message




def SendResetEmail(user):
    token = user.GenerateToken()
    msg = Message('Password Reset Request', 
                  sender='flaskblog.rhschuld@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''To rest your password, visit the following link:

    {url_for('ResetWithToken', token=token, _external=True)}
    
    If you did not make this request then simply ignore this email and no change will be made
    '''
    mail.send(msg)
