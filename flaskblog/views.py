from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Posts

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('Home'))
    return render_template('register.html', title = 'Register', form=form)

@app.route("/login", methods=['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('Home'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html', title = 'Login', form=form)


