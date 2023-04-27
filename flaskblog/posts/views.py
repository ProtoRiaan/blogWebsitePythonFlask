


from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.forms import PostForm
from flaskblog.models import Posts
from flask_login import current_user, login_required



from flask import Blueprint

posts = Blueprint('posts',__name__)


@posts.route("/blog")
def Blog():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)

@posts.route("/posts/new", methods=['GET', 'POST'])
@login_required
def NewPost():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!','success')
        post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Blog'))
    return render_template('create_post.html', title='New Post"', form=form,
                           legend='New Post')


@posts.route("/posts/<int:postID>")
def Post(postID):
    post = Posts.query.get_or_404(postID)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/posts/<int:postID>/update", methods=['GET','POST'])
@login_required
def PostUpdate(postID):
    post = Posts.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('Post', postID=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update ' + post.title, form=form,
                           legend='Update Post')

@posts.route("/post/<int:postID>/delete", methods=['POST'])
@login_required
def PostDelete(postID):
    post = Posts.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    db.session.delete((post))
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('Blog'))




