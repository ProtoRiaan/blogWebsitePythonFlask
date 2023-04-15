from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Riaan Schuld',
        'title': 'Blogpost Test1',
        'content': 'Test for post 1',
        'datePosted' : 'April 2nd 2023'
    },
    {
        'author': 'Diana Collins',
        'title': 'Blogpost Test2',
        'content': 'Test for post 2',
        'datePosted' : 'April 2nd 2023'
    }
]

@app.route("/")
@app.route("/home")
def Home():
    return render_template('home.html', title = 'Home')


@app.route("/about")
def About():
    return render_template('about.html', title = 'About')

@app.route("/blog")
def Blog():
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

@app.route("/account")
@login_required
def Account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file)
