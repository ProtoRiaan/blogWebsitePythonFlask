

import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ResetConfigForm, ResetRequestForm
from flaskblog.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



@app.route("/")
@app.route("/home")
def Home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def About():
    return render_template('about.html', title = 'About')

@app.route("/blog")
def Blog():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)

@app.route("/archive")
def Archive():
    return render_template('archive.html', title = 'Archive')

@app.route("/register", methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'success')
        return redirect(url_for('Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Log in to get started!', 'success')
        return redirect(url_for('Login'))
    return render_template('register.html', title = 'Register', form=form)

@app.route("/login", methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'success')
        return redirect(url_for('Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Your login was successful!', 'success')
            #remembers when @login_required redirects and returns back after successfully login, else sends you home(for standard logins)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('Home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html', title = 'Login', form=form)

@app.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for('Home'))

def Save_Picture(formPicture):

    #delete old profile pic from disk if it is not default.jpg and exists
    currentPicturePath = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(currentPicturePath) and current_user.image_file != 'default.jpg':
        os.remove(currentPicturePath)

    #create random file name for new image file
    random_hex = secrets.token_hex(8)
    _, fileEXT = os.path.splitext(formPicture.filename)
    pictureFileName = random_hex + fileEXT
    picturePath = os.path.join(app.root_path, 'static/profile_pics', pictureFileName)

    #shrink image file and write to disk
    outputSize = (125,125)
    standardImage = Image.open(formPicture)
    standardImage.thumbnail(outputSize)
    standardImage.save(picturePath)

    return pictureFileName

@app.route("/account", methods=['GET','POST'])
@login_required
def Account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = Save_Picture(form.picture.data)
            current_user.image_file = pictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)

@app.route("/posts/new", methods=['GET', 'POST'])
@login_required
def NewPost():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!','success')
        post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Blog'))
    return render_template('create_post.html', title='New Post"', form=form,
                           legend='New Post')


@app.route("/posts/<int:postID>")
def Post(postID):
    post = Posts.query.get_or_404(postID)
    return render_template('post.html', title=post.title, post=post)

@app.route("/posts/<int:postID>/update", methods=['GET','POST'])
@login_required
def PostUpdate(postID):
    post = Posts.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('Post', postID=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update ' + post.title, form=form,
                           legend='Update Post')

@app.route("/post/<int:postID>/delete", methods=['POST'])
@login_required
def PostDelete(postID):
    post = Posts.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    db.session.delete((post))
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('Blog'))

@app.route("/user/<string:username>")
def UserPost(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user)\
        .order_by(Posts.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user.html', posts=posts, user=user)


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

@app.route("/reset_password", methods=['GET','POST'])
def ResetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        flash('debug helper : we made it this far')
        SendResetEmail(user)
        flash ('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('Login'))

    return render_template('reset_request.html', title = 'Reset Password', form=form)
        

@app.route("/reset_password/<token>", methods=['GET','POST'])
def ResetWithToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    user = User.ConfirmToken(token)
    if user is False:
        flash('Your password reset request is invalid or has expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetConfigForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Log in to get started!', 'success')
        return redirect(url_for('Login'))

    return render_template('reset_with_token.html', title = 'Reset Password', form=form)
