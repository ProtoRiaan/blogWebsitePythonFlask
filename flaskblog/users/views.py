

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog import db, bcrypt
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetConfigForm, ResetRequestForm
from flaskblog.models import User
from flaskblog.users.userfunctions import SendResetEmail, Save_Picture
from flask_login import login_user, current_user, logout_user, login_required



users = Blueprint('users',__name__)

#Register route
@users.route("/register", methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'success')
        return redirect(url_for('main.Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Log in to get started!', 'success')
        return redirect(url_for('users.Login'))
    return render_template('register.html', title = 'Register', form=form)

#Login Route
@users.route("/login", methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'success')
        return redirect(url_for('main.Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Your login was successful!', 'success')
            #remembers when @login_required redirects and returns back after successfully login, else sends you home(for standard logins)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('main.Home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html', title = 'Login', form=form)

#Logout Route
@users.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for('main.Home'))



@users.route("/account", methods=['GET','POST'])
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
        return redirect(url_for('users.Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)

@users.route("/reset_password", methods=['GET','POST'])
def ResetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('main.Home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        SendResetEmail(user)
        flash ('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('users.Login'))

    return render_template('reset_request.html', title = 'Reset Password', form=form)
        

@users.route("/reset_password/<token>", methods=['GET','POST'])
def ResetWithToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.Home'))
    user = User.ConfirmToken(token)
    if user is False:
        flash('Your password reset request is invalid or has expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetConfigForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Log in to get started!', 'success')
        return redirect(url_for('users.Login'))

    return render_template('reset_with_token.html', title = 'Reset Password', form=form)


