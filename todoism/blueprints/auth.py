# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: auth.py
    @time: 2020/2/9
    @desc: 用户认证模块
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from faker import Faker

from todoism.extensions import db
from todoism.models import User, Item

auth_bp = Blueprint('auth', __name__)
fake = Faker()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))

    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        # 先找到是否有这个用户
        user = User.query.filter_by(username=username).first()

        # 在验证密码
        if user is not None and user.validate_password(password):
            login_user(user)  # flask_login的工具函数, 根据用户ID与其他值生成session
            return jsonify(message='Login success')
        return jsonify(message='Invalid username or password'), 400
    return render_template('_login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='Logout success.')


@auth_bp.route('/register')
def register():
    # 由于是demo, 用 faker 生成随机账户
    username = fake.user_name()
    # 为防止随机账户名跟数据库中的冲突, 循环检测
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()

    # 创建随机用户到数据库
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # 创建随机Todo Items到数据库
    item1 = Item(body='Witness something truly majestic', author=user)
    item2 = Item(body='Help a complete stranger', author=user)
    item3 = Item(body='Drive a motorcycle on the Great Wall of China', author=user)
    item4 = Item(body='Sit on the Great Egyptian Pyramids', done=True, author=user)
    db.session.add_all([item1, item2, item3, item4])
    db.session.commit()

    return jsonify(username=username, password=password, message='Generate success.')
