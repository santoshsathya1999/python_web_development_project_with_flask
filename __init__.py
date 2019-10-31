# companyblog/init.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#Create an instance of Flask
app = Flask(__name__)

################################################
############# CREATE DATABASE ##################
################################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='thisismysecretkey'

db = SQLAlchemy(app)
Migrate(app,db)

###############################################
############# LOGIN CONFIG ####################
###############################################

# create instance of LoginManager
login_manager = LoginManager()
# pass in the app
login_manager.init_app(app)
# tell users whta view to go to when they log in
login_manager.login_view = 'users.login'


##############################################
############## BLUEPRINTS ####################
##############################################

from companyblog.core.views import core
from companyblog.error_pages.handlers import error_pages
from companyblog.users.views import users
from companyblog.blog_posts.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)

