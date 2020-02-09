# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: models.py
    @time: 2020/2/8
    @desc: DB Models
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from todoism.extensions import db


# 用户模型类
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', back_populates='author', cascade='all')  # 1对多关系双向绑定+删除级联

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # 使用 hash 加密密码

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 目标模型类
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 定义author_id外键
    author = db.relationship('User', back_populates='items')  # 1对多关系双向绑定
