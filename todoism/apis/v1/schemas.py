# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: schemas.py
    @time: 2020/2/8
    @desc: 返回到前端的数据结构
"""
from flask import url_for


def user_schema(user):
    return {
        'id': user.id,
        'self': url_for('.user', _external=True),
        'kind': 'User',
        'username': user.username,
        # 'all_items_url': url_for('.items', _external=True),
    }


def item_schema(item):
    return {
        'id': item.id,
        'self': url_for('.item', item_id=item.id, _external=True),
        'kind': 'Item',
        'body': item.body,
        'done': item.done,
        'author': {
            'id': item.author_id,
            'url': url_for('.user', _external=True),
            'username': item.author.username,
            'kind': 'User',
        },
    }
