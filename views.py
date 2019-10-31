from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required

from companyblog import db
from companyblog.models import User, BlogPost
from companyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from companyblog.users.picture_handler import add_profile_pic

########################################
# ######################################
# REGISTER
# LOGIN
# UPDATE PROFILE
# LOGOUT
# USER LIST OF BLOG POSTS
########################################
########################################

# Create Blueprint => register in company/__init__.py
users = Blueprint('users', __name__)

#########################################
############# logout ####################
#########################################

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index')) # core.index Blueprint

# Register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

########################################
############# Login ####################
########################################

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user) 
            flash('You successfully logged in')
            
            # if user has been redirected from another page 
            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')
                return redirect(next)
    return render_template('login.html', form=form)

################################################
################# Update account ###############
################################################

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
    # Check if there is a picture upload
        if form.picture.data:
            username = current_user.username
            #pass to the add_profile_pic function in picture handler
            # where the image is saved to the static folder
            pic = add_profile_pic(form.picture.data,username)
            #set the image to the profile image attribute in the User 
            current_user.profile_image = pic
        #set the username and email from the form data
        current_user.username = form.username.data
        current_user.email = form.email.data
        # save to the database
        db.session.commit()
        flash('User account updated')
        return redirect(url_for('core.index'))
    # First time page is hit get populate with the  current data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # The profile image will either be the unchanged image if it hasn't been updated
    # or the updated image saved to the static/profile_pic
    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', form=form, profile_image=profile_image)

###############################################
################ POSTS ######################## 
###############################################

@users.route('/<username>')
def user_posts(username):
    # for pagination
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_post.html',blog_posts=blog_posts, user=user)





    


