

from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, abort, session
from flaskblog import db, bcrypt
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetConfigForm, ResetRequestForm
from flaskblog.models import User
from flaskblog.users.userfunctions import SendResetEmail, Save_Picture
from flask_login import login_user, current_user, logout_user, login_required
import requests
import secrets
from urllib.parse import urlencode


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

#Google Login

@users.route('/authorize/<provider>',methods=['GET'])
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('users.oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)



@users.route('/callback/<provider>',methods=['GET'])
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.Home'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('main.Home'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('users.oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    # find or create the user in the database
    user = db.session.scalar(db.select(User).where(User.email == email))
    if user is None:
        hashed_password = bcrypt.generate_password_hash(secrets.token_urlsafe(14)).decode('utf-8)')
        user = User(email=email, username=email.split('@')[0], password=hashed_password)
        db.session.add(user)
        db.session.commit()

    # log the user in
    login_user(user)
    return redirect(url_for('main.Home'))