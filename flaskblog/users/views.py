from flask import Blueprint

users = Blueprint('users',__name__)


@users.route("/register", methods=['GET','POST'])
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

@users.route("/login", methods=['GET','POST'])
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

@users.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for('Home'))

def Save_Picture(formPicture):

    #delete old profile pic from disk if it is not default.jpg and exists
    currentPicturePath = os.path.join(users.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(currentPicturePath) and current_user.image_file != 'default.jpg':
        os.remove(currentPicturePath)

    #create random file name for new image file
    random_hex = secrets.token_hex(8)
    _, fileEXT = os.path.splitext(formPicture.filename)
    pictureFileName = random_hex + fileEXT
    picturePath = os.path.join(users.root_path, 'static/profile_pics', pictureFileName)

    #shrink image file and write to disk
    outputSize = (125,125)
    standardImage = Image.open(formPicture)
    standardImage.thumbnail(outputSize)
    standardImage.save(picturePath)

    return pictureFileName

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
        return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)

@users.route("/reset_password", methods=['GET','POST'])
def ResetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        SendResetEmail(user)
        flash ('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('Login'))

    return render_template('reset_request.html', title = 'Reset Password', form=form)
        

@users.route("/reset_password/<token>", methods=['GET','POST'])
def ResetWithToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    user = User.ConfirmToken(token)
    if user is False:
        flash('Your password reset request is invalid or has expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetConfigForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Log in to get started!', 'success')
        return redirect(url_for('Login'))

    return render_template('reset_with_token.html', title = 'Reset Password', form=form)


@users.route("/user/<string:username>")
def UserPost(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user)\
        .order_by(Posts.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user.html', posts=posts, user=user)

