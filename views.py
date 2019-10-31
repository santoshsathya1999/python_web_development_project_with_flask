# blog_post/views.py

from flask import render_template, redirect, request, url_for, Blueprint, flash, abort
from flask_login import login_user, current_user, logout_user, login_required

from companyblog import db
from companyblog.models import BlogPost
from companyblog.blog_posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts',__name__)

################################
########## CREATE POST #########
################################
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        # INSTANCE OF BLOGPOST
        blog_post = BlogPost(title=form.title.data,
                             text = form.text.data,
                             user_id=current_user.id)
        # SAVE TO DATABASE
        db.session.add(blog_post)
        db.session.commit()
        flash('Post Created')
        return redirect(url_for('core.index'))
        
    return render_template('create_post.html', form=form)

########################################
########### BLOG POST (VIEW) ###########
########################################

@blog_posts.route('/<int:blog_post_id>', methods = ['GET', 'POST'])
def blog_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', post=post,
                            title=post.title,
                            date=post.date) 

######################################
############## UPDATE ################
######################################

@blog_posts.route('/<int:blog_post_id>/update', methods = ['GET', 'POST'])
@login_required
def update(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    if post.author != current_user:
        abort(403)
    
    form = BlogPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        
        db.session.add(post)
        db.session.commit()

        flash('Blog Post Updated')

        return redirect(url_for('blog_posts.blog_post',blog_post_id=post.id))
    else:
        # if hitting the page for the first time
        if request.method == 'GET':
            form.title.data = post.title
            form.text.data = post.text
        
    return render_template('create_post.html', form=form, title='Update Post')

########################################
############# DELETE ###################
########################################
'''
this view does'nt have a html associated with it, rather  a
dropdown option on the edit page for blog deletion. Therefore there is 
no 'delete.html'
'''
@blog_posts.route('/<int:blog_post_id>/delete', methods = ['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')
    return redirect(url_for('core.index'))



