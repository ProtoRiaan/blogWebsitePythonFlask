

from flask import Blueprint

main = Blueprint('posts',__name__)


@main.route("/")
@main.route("/home")
def Home():
    return render_template('home.html', title = 'Home')


@main.route("/about")
def About():
    return render_template('about.html', title = 'About')


@main.route("/archive")
def Archive():
    return render_template('archive.html', title = 'Archive')
