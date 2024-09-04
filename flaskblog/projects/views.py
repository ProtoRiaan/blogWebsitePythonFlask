
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import db
from flaskblog.models import projects_data
from flask_login import current_user, login_required


projects = Blueprint('projects',__name__)


@projects.route("/projects")
def Projects():
    projects = projects_data
    return render_template('projects/projects.html', project=projects)

@projects.route("/projects_admin")
@login_required
def Projects_Admin():
    projects = projects_data
    return render_template('projects/projects_admin.html', project=projects)

