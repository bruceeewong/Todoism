# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: extensions.py
    @time: 2020/2/8
    @desc: 
"""
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()  # 实例化 SQLAlchemy
csrf = CSRFProtect()  # 添加CSRF插件

login_manager = LoginManager() # 添加flask_login插件
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page'


# The user_loader callback is used to reload the user object
# from the user ID stored in the session.
@login_manager.user_loader
def loader_user(user_id):
    """login_manager要实现的函数,用于通过ID获取自定义的User对象"""
    from todoism.models import User
    return User.query.get(int(user_id))
