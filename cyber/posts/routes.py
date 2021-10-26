from flask import Blueprint, render_template, request,  url_for, redirect, jsonify, abort
from flask_login import current_user, login_required
from cyber.models import Post
from cyber.posts.forms import PostForm
from cyber import db

Posts = Blueprint('posts', __name__)

@Posts.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == 'POST':
        try:
            data = request.form['aim']
            post = Post.query.filter(Post.title.like('%'+data+'%')).first()
            data = { 'id': post.id, 'title': post.title}
            return jsonify(data)
        except:
            pass
    posts = reversed(Post.query.all())
    return render_template('main/posts.html', posts=posts, title='posts')

@Posts.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.posts'))
    return render_template('main/new_post.html', form=form, title='new post')

@Posts.route('/posts/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    social = {'decsription': post.description, 'image': str(post.author.user_img)}
    return render_template('main/post.html', post=post, title=str(post.title), social=social)

@Posts.route('/posts/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.posts'))
