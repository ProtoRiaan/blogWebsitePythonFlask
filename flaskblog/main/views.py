

import os
from flask import Blueprint,render_template,send_from_directory,current_app

main = Blueprint('main',__name__)


@main.route("/")
@main.route("/home")
def Home():
    return render_template('home.html', title = 'Home')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route("/about")
def About():
    return render_template('about.html', title = 'About')


@main.route("/archive")
def Archive():
    return render_template('archive.html', title = 'Archive')
