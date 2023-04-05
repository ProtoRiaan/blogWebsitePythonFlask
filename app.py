

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = '65642ab665b75a1abf898a329f9327f4'

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

@app.route("/register", methods=['GET','POST'])
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('Home'))
    return render_template('register.html', title = 'Register', form=form)

@app.route("/login")
def Login():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form=form)



if __name__ == '__main__':
    app.run(debug=True)

