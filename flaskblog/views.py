

import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostFrom
from flaskblog.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def Home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def About():
    return render_template('about.html', title = 'About')

@app.route("/blog")
def Blog():
    posts = Posts.query.all()
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
    form = PostFrom()
    if form.validate_on_submit():
        flash('Your post has been created!','success')
        post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Home'))
    return render_template('create_post.html', title='New Post"', form=form)
