# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: test_app.py
    @time: 2020/2/8
    @desc: 生成测试数据. 可先运行flask run, 再from test_app import app即可拥有测试数据
"""
from todoism import create_app, db
from todoism.models import User, Item

app = create_app('testing')

with app.app_context():
    db.create_all()

    user = User(username='bruski')
    user.set_password('123')
    db.session.add(user)

    item1 = Item(body='test item 1')
    item2 = Item(body='test item 2')
    item3 = Item(body='test item 3')
    item4 = Item(body='test item 4', done=True)
    user.items = [item1, item2, item3, item4]

    db.session.commit()
