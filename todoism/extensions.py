# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: extensions.py
    @time: 2020/2/8
    @desc: 
"""
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# 实例化 SQLAlchemy

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page'


# The user_loader callback is used to reload the user object
# from the user ID stored in the session.
@login_manager.user_loader
def loader_user(user_id):
    from todoism.models import User
    return User.query.get(int(user_id))
