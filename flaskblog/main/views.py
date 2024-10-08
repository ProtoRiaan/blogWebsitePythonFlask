

from flask import Blueprint,render_template,current_app,send_from_directory

import markdown
import os

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
    aboutMDPath = os.path.join(current_app.root_path, 'static/about/about.md')
    hobbiesMDPath = os.path.join(current_app.root_path, 'static/about/hobbies.md')
    certs = current_app.config['CERTS']
    with open(aboutMDPath) as mdfile:
        experiencemd = markdown.markdown(mdfile.read(), extensions=['fenced_code','codehilite'])
    with open(hobbiesMDPath) as mdfile:
        hobbiesmd = markdown.markdown(mdfile.read(), extensions=['fenced_code','codehilite'])
    return render_template('about.html', title = 'About', experiencemd=experiencemd, hobbiesmd=hobbiesmd, certs=certs)


@main.route("/archive")
def Archive():
    return render_template('archive.html', title = 'Archive')
