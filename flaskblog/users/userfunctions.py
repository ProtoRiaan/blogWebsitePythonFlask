
import os, secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message
from flask_login import current_user




def SendResetEmail(user):
    token = user.GenerateToken()
    msg = Message('Password Reset Request', 
                  sender='flaskblog.rhschuld@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''To rest your password, visit the following link:

    {url_for('users.ResetWithToken', token=token, _external=True, _scheme='https')}
    
    If you did not make this request then simply ignore this email and no change will be made
    '''
    mail.send(msg)


def Save_Picture(formPicture):

    #delete old profile pic from disk if it is not default.jpg and exists
    currentPicturePath = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(currentPicturePath) and current_user.image_file != 'default.jpg':
        os.remove(currentPicturePath)

    #create random file name for new image file
    random_hex = secrets.token_hex(8)
    _, fileEXT = os.path.splitext(formPicture.filename)
    pictureFileName = random_hex + fileEXT
    picturePath = os.path.join(current_app.root_path, 'static/profile_pics', pictureFileName)

    #shrink image file and write to disk
    outputSize = (125,125)
    standardImage = Image.open(formPicture)
    standardImage.thumbnail(outputSize)
    standardImage.save(picturePath)

    return pictureFileName